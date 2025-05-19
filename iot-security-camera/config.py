"""
Configuration settings for the IoT security camera system.
"""
import os

# Certificate paths
CERT_PATH = "certs"
PATH_TO_AMAZON_ROOT_CA_1 = os.path.join(CERT_PATH, "AmazonRootCA1.pem")
PATH_TO_CERTIFICATE = os.path.join(CERT_PATH, "root.pem")
PATH_TO_PRIVATE_KEY = os.path.join(CERT_PATH, "1861f71c931055d2efb5687c16278b1e4bdda96a39a7aaa1f3636b3fe592f2ee-private.pem.key")

# AWS IoT settings
ENDPOINT = "a3e9lka9w5gk8f-ats.iot.ap-southeast-2.amazonaws.com"
CLIENT_ID = "iot_edge_device1"
TOPIC_ALERT = "security/camera/alerts"
RANGE = 20

# Local storage directories
CLIPS_DIR = "clips"
FRAMES_DIR = "frames"

# S3 bucket configuration
S3_BUCKET = "jalil-iot-project"

# Frame extraction settings
FRAMES_TO_EXTRACT = 3
RECORDING_DURATION = 20  # seconds

# Privacy mode settings
PRIVACY_COMMAND_TOPIC = "home/cameras/privacy/command"
PRIVACY_STATUS_TOPIC = "home/cameras/privacy/status"
PRIVACY_STATE_FILE = "privacy_state.json"

# Livestream settings
STREAM_COMMAND_TOPIC = "home/cameras/livestream/command"
STREAM_STATUS_TOPIC = "home/cameras/livestream/status"

# Motion detection thresholds
MOTION_SPEED_THRESHOLD = 0.1  # m/s
MOTION_RANGE_THRESHOLD = 80   # cm
MOTION_ENERGY_THRESHOLD = 5
MOTION_BAUD_RATE = 9600
