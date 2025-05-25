# IoT Security Camera System

A comprehensive IoT-based security camera system with motion detection, real-time streaming, cloud integration, and intelligent object detection. Built for Raspberry Pi edge devices with a modern web interface and AWS cloud backend.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Edge Device   │────│   Middleware    │────│ Web Application │
│  (Raspberry Pi) │    │   (Node.js)     │    │     (React)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  AWS Services   │
                    │ • IoT Core      │
                    │ • S3 Storage    │
                    │ • Lambda        │
                    │ • Rekognition   │
                    │ • SNS           │
                    └─────────────────┘
```

## ✨ Features

### 🎥 Edge Device (Raspberry Pi)
- **Motion Detection**: DFRobot C4001 mmWave radar sensor for precise detection
- **Video Recording**: Automatic 20-second clips when motion is detected
- **Live Streaming**: Real-time video feed via web interface (port 8080)
- **Frame Extraction**: Thumbnail generation for AI analysis
- **Privacy Mode**: Remote camera control via MQTT
- **Cloud Upload**: Automatic upload to AWS S3

### 🔄 Middleware (Node.js/Express)
- **Video Management**: Serve videos from S3 with signed URLs
- **Real-time Communication**: WebSocket and Socket.IO for live updates
- **Privacy Controls**: Toggle camera privacy mode remotely
- **AWS Integration**: IoT Core MQTT and S3 communication
- **Notification System**: Real-time alerts and status updates

### 🌐 Web Application (React)
- **Video Gallery**: Browse recorded footage with thumbnail previews
- **Live Streaming**: Real-time camera feed display
- **Dark/Light Theme**: Responsive theme switching
- **Notification Panel**: Live security event notifications
- **Mobile-Friendly**: Responsive design with collapsible sidebar

### ☁️ Cloud Functions (AWS Lambda)
- **AI Object Detection**: AWS Rekognition for intelligent analysis
- **Smart Notifications**: SMS alerts for important detections (Person, Vehicle, etc.)
- **Confidence Filtering**: 70% minimum confidence threshold
- **Dual Notifications**: Both IoT and SMS alerts

## 🛠️ Technology Stack

| Component | Technologies |
|-----------|-------------|
| **Edge Device** | Python 3.8+, Raspberry Pi Camera, DFRobot C4001 |
| **Middleware** | Node.js, TypeScript, Express.js, Socket.IO |
| **Web App** | React 19, TypeScript, Vite, Tailwind CSS |
| **Cloud** | AWS IoT Core, S3, Lambda, Rekognition, SNS |
| **Communication** | MQTT, WebSocket, REST API |

## 🚀 Quick Start

### Prerequisites
- Raspberry Pi 4 with Camera Module
- DFRobot C4001 Motion Sensor
- AWS Account with IoT Core, S3, Lambda access
- Node.js 18+ for middleware and web app

### 1. Edge Device Setup

```bash
cd edge-device
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure AWS certificates in certs/ directory
# Update config.py with your AWS settings
python entrypoint.py
```

### 2. Middleware Setup

```bash
cd middleware
npm install
cp .env.example .env
# Configure AWS credentials in .env
npm run dev
```

### 3. Web Application Setup

```bash
cd web-application
npm install
npm run dev
```

### 4. AWS Cloud Functions

Deploy `cloud-functions/lambda.py` to AWS Lambda with:
- S3 trigger for frames upload
- Rekognition, SNS, IoT permissions
- Environment variables configured

## 📁 Project Structure

```
cits5506-proj/
├── edge-device/           # Raspberry Pi camera system
│   ├── camera/           # Video recording and management
│   ├── cloud/            # AWS IoT and S3 integration
│   ├── motion/           # Motion detection with DFRobot sensor
│   ├── privacy/          # Privacy mode management
│   ├── streaming/        # Live video streaming
│   └── config.py         # System configuration
├── middleware/           # Node.js backend server
│   ├── src/routes/       # API endpoints (video, privacy)
│   ├── src/services/     # IoT and WebSocket services
│   └── certs/            # AWS IoT certificates
├── web-application/      # React frontend
│   ├── src/components/   # UI components
│   ├── src/pages/        # Main application pages
│   └── src/utils/        # Utilities and contexts
└── cloud-functions/      # AWS Lambda functions
    └── lambda.py         # Object detection and notifications
```

## 🔧 Configuration

### Edge Device Configuration (`edge-device/config.py`)
```python
# AWS IoT settings
ENDPOINT = "your-iot-endpoint.iot.region.amazonaws.com"
CLIENT_ID = "your-device-id"
S3_BUCKET = "your-s3-bucket"

# Recording settings
RECORDING_DURATION = 20  # seconds
FRAMES_TO_EXTRACT = 3
MOTION_DETECTION_COOLDOWN = 5
```

### Middleware Environment (`.env`)
```env
AWS_REGION=ap-southeast-2
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=your-s3-bucket
PORT=3000
```

## 📡 MQTT Topics

| Topic | Purpose |
|-------|---------|
| `home/cameras/privacy/command` | Privacy mode control |
| `home/cameras/privacy/status` | Privacy status updates |
| `home/cameras/livestream/command` | Streaming control |
| `home/cameras/notification` | Camera notifications |
| `security/camera/alerts` | Motion detection alerts |

## 🚨 Security Features

- **Privacy Mode**: Complete camera shutdown capability
- **Certificate-based Authentication**: AWS IoT device certificates
- **Signed URLs**: Temporary S3 access with 24-hour expiry
- **Intelligent Filtering**: AI-powered object detection with confidence thresholds
- **Secure Communication**: MQTT over TLS, HTTPS endpoints

## 📱 API Endpoints

### Video Management
- `GET /videos` - List all videos with thumbnails
- `GET /thumbnails/frames/:dateStr/frame_:frameNum.jpg` - Serve thumbnails

### Privacy Control
- `GET /status` - Get privacy mode status
- `POST /set` - Toggle privacy mode

## 🔍 Monitoring & Debugging

### View Edge Device Logs
```bash
cd edge-device
python entrypoint.py 2>&1 | tee system.log
```

### Monitor Middleware
```bash
cd middleware
npm run dev  # Development with hot reload
```

### Check AWS Lambda Logs
```bash
aws logs tail /aws/lambda/your-function-name --follow
```

## 🛡️ Troubleshooting

### Common Issues

**Camera Not Working**
- Enable camera in `raspi-config`
- Check camera cable connections
- Verify permissions: `sudo usermod -a -G video $USER`

**Motion Sensor Issues**
- Enable UART in `raspi-config`
- Verify sensor wiring (TX→GPIO14, RX→GPIO15)
- Check baud rate configuration (9600)

**AWS Connection Problems**
- Verify certificate files in `certs/` directory
- Check IoT endpoint and region settings
- Ensure IoT policies allow required actions

**Performance Issues**
- Use Class 10+ MicroSD card
- Monitor CPU temperature
- Adjust motion detection thresholds

## 📄 License

This project is licensed under the ISC License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For hardware-specific issues:
- **Raspberry Pi Camera**: [Official Documentation](https://www.raspberrypi.org/documentation/configuration/camera.md)
- **DFRobot C4001**: [GitHub Repository](https://github.com/DFRobot/DFRobot_C4001)

For AWS services:
- **IoT Core**: [AWS IoT Documentation](https://docs.aws.amazon.com/iot/)
- **Rekognition**: [AWS Rekognition Documentation](https://docs.aws.amazon.com/rekognition/)