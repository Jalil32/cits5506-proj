# IoT Security Camera System - Edge Device

A Python-based IoT security camera system designed for Raspberry Pi that provides motion detection, video recording, live streaming, and cloud integration.

## Features

- **Motion Detection**: Uses DFRobot C4001 mmWave radar sensor for precise motion detection
- **Video Recording**: Captures video clips when motion is detected
- **Live Streaming**: Provides real-time video streaming via web interface
- **Cloud Integration**: Uploads recordings to AWS S3 and sends alerts via AWS IoT MQTT
- **Privacy Mode**: Toggle camera functionality on/off remotely
- **Frame Extraction**: Generates thumbnail frames from recorded videos

## Hardware Requirements

- Raspberry Pi (tested with Pi 4)
- Raspberry Pi Camera Module
- DFRobot C4001 mmWave Motion Detection Sensor
- MicroSD card (32GB+ recommended)

## Software Requirements

- Python 3.8+
- Raspberry Pi OS (Bullseye or newer recommended)

## Installation

### 1. System Dependencies

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-pip python3-venv git

# Enable camera interface
sudo raspi-config
# Navigate to: Interfacing Options → Camera → Enable

# Reboot to apply camera settings
sudo reboot
```

### 2. Python Environment Setup

```bash
# Clone the repository (if not already done)
cd /path/to/your/project

# Navigate to edge-device directory
cd edge-device

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. AWS Configuration

#### 3.1 Create AWS Certificates
1. Create an AWS IoT Thing in your AWS console
2. Download the certificate files and place them in the `certs/` directory:
   - `AmazonRootCA1.pem`
   - `root.pem` (device certificate)
   - `<device-private-key>.pem.key` (private key)

#### 3.2 Update Configuration
Edit `config.py` to match your AWS setup:

```python
# Update these values in config.py
ENDPOINT = "your-aws-iot-endpoint.iot.region.amazonaws.com"
CLIENT_ID = "your-device-id"
PATH_TO_PRIVATE_KEY = "certs/your-private-key.pem.key"
S3_BUCKET = "your-s3-bucket-name"
```

### 4. Hardware Setup

#### 4.1 Camera Connection
- Connect the Raspberry Pi Camera Module to the camera port on your Raspberry Pi

#### 4.2 Motion Sensor Connection
Connect the DFRobot C4001 sensor:
- VCC → 3.3V or 5V
- GND → Ground
- TX → GPIO 14 (UART RX)
- RX → GPIO 15 (UART TX)

Enable UART in Raspberry Pi:
```bash
sudo raspi-config
# Navigate to: Interfacing Options → Serial → Enable
sudo reboot
```

## Usage

### Running the System

```bash
# Activate virtual environment
source venv/bin/activate

# Run the main application
python entrypoint.py
```

### System Behavior

1. **Startup**: Initializes camera, motion sensor, and cloud connections
2. **Detection Loop**: Continuously monitors for motion
3. **Motion Response**: When motion is detected:
   - Records video clip (20 seconds by default)
   - Extracts thumbnail frames
   - Uploads to AWS S3
   - Sends alert via MQTT
4. **Live Streaming**: Provides web interface at `http://device-ip:8080`

### Privacy Mode

Control privacy mode via MQTT:
```bash
# Enable privacy mode (stops all recording/streaming)
mosquitto_pub -h your-mqtt-broker -t "home/cameras/privacy/command" -m '{"command": "enable", "client_id": "your-device-id"}'

# Disable privacy mode
mosquitto_pub -h your-mqtt-broker -t "home/cameras/privacy/command" -m '{"command": "disable", "client_id": "your-device-id"}'
```

### Live Streaming Control

Control streaming via MQTT:
```bash
# Start live stream
mosquitto_pub -h your-mqtt-broker -t "home/cameras/livestream/command" -m '{"command": "start", "client_id": "your-device-id"}'

# Stop live stream
mosquitto_pub -h your-mqtt-broker -t "home/cameras/livestream/command" -m '{"command": "stop", "client_id": "your-device-id"}'
```

## Configuration

Key configuration options in `config.py`:

- `RECORDING_DURATION`: Video recording length (default: 20 seconds)
- `FRAMES_TO_EXTRACT`: Number of thumbnail frames (default: 3)
- `MOTION_DETECTION_COOLDOWN`: Delay between detections (default: 5 seconds)
- `STREAM_PORT`: Live stream web server port (default: 8080)

## Project Structure

```
edge-device/
├── camera/              # Camera management and video recording
├── cloud/               # AWS IoT MQTT and S3 integration
├── motion/              # Motion detection using DFRobot sensor
├── privacy/             # Privacy mode management
├── streaming/           # Live video streaming
├── utils/               # Logging and file utilities
├── config.py            # Configuration settings
├── entrypoint.py        # Main application entry point
└── requirements.txt     # Python dependencies
```

## Troubleshooting

### Camera Issues
- Ensure camera is enabled: `sudo raspi-config`
- Check camera connection and cables
- Verify camera permissions: `sudo usermod -a -G video $USER`

### Motion Sensor Issues
- Verify UART is enabled in raspi-config
- Check sensor wiring and power supply
- Ensure correct baud rate (9600) in config

### AWS Connection Issues
- Verify certificate files are in the correct location
- Check AWS IoT endpoint and region settings
- Ensure IoT policies allow required actions

### Performance Issues
- Use Class 10 MicroSD card for better I/O performance
- Consider adjusting motion detection thresholds
- Monitor CPU temperature and ensure adequate cooling

## Logs

System logs are written to stdout and can be captured:

```bash
# Run with log file
python entrypoint.py 2>&1 | tee system.log

# View logs in real-time
tail -f system.log
```

## Security Notes

- Keep AWS certificates secure and never commit them to version control
- Use strong passwords for any remote access
- Regularly update system packages and dependencies
- Consider using AWS IAM roles with minimal required permissions

## Support

For issues specific to hardware components:
- Raspberry Pi Camera: Official Raspberry Pi documentation
- DFRobot C4001: [DFRobot official repository](https://github.com/DFRobot/DFRobot_C4001)
