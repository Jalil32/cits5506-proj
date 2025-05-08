import boto3
from awscrt import io, mqtt, auth, http 
from awsiot import mqtt_connection_builder 
import os 
import time
import json
import logging
from datetime import datetime
import cv2

# Certificate paths
CERT_PATH = "certs"
PATH_TO_AMAZON_ROOT_CA_1 = os.path.join(CERT_PATH, "AmazonRootCA1.pem")
PATH_TO_CERTIFICATE = os.path.join(CERT_PATH, "root.pem")  # This should be your device certificate
PATH_TO_PRIVATE_KEY = os.path.join(CERT_PATH, "1861f71c931055d2efb5687c16278b1e4bdda96a39a7aaa1f3636b3fe592f2ee-private.pem.key")

# AWS IoT 
ENDPOINT = "a3e9lka9w5gk8f-ats.iot.ap-southeast-2.amazonaws.com"
CLIENT_ID = "iot_edge_device1"
TOPIC = "security/camera/alerts"
RANGE = 20

# Edge Camera
CLIPS_DIR = "clips"

# Camera Index
CAMERA_INDEX = 0

# Fixed S3 bucket name - removed "s3://" prefix and trailing slash
S3_BUCKET = "jalil-iot-project"

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=30
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))

connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

# Set up S3 client
s3_client = boto3.client('s3')

def setup_logger(log_level=logging.INFO):
    """Set up and configure a basic logger.
    
    Args:
        log_level: The logging level (default: logging.INFO)
    
    Returns:
        A configured logger instance
    """
    # Create a logger
    logger = logging.getLogger('my_application')
    logger.setLevel(log_level)
    
    # Create console handler and set level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    return logger

# Function to upload file to s3
def upload_to_s3(local_file, s3_key):
    print(f"Uploading {local_file} to S3 bucket {S3_BUCKET}")
    try:
        s3_client.upload_file(local_file, S3_BUCKET, s3_key)
        s3_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"
        print(f"Upload complete: {s3_url}")
        return s3_url
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

# Function to send MQTT notification
def send_notification(s3_url, timestamp):
    message = {
        "device_id": CLIENT_ID,
        "alert": "Motion detected",
        "timestamp": timestamp,
        "video_url": s3_url
    }
    
    mqtt_connection.publish(
        topic=TOPIC,
        payload=json.dumps(message),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

def detect_motion():
    # Aneesh to implement this
    return True

def record_clip(filename, duration, camera):
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use mp4v codec for Mac compatibility
    fps = 20.0
    frame_size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(filename, fourcc, fps, frame_size)
    
    start_time = time.time()
    end_time = start_time + duration
    
    while time.time() < end_time:
        ret, frame = camera.read()
        if ret:
            out.write(frame)
        else:
            break
    
    # Make sure to release the VideoWriter
    out.release()
    
    return filename

def main():
    logger = setup_logger()

    # 1) Connect to camera    
    # Initialize webcam
    logger.info("Initialising camera...")
    camera = cv2.VideoCapture(CAMERA_INDEX)
    
    if not camera.isOpened():
        logger.error("Could not open camera")
        print("Error: Could not open webcam")
        return
    
    # Set camera resolution
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    logger.info("Camera initialized successfully")

    try:
        # Create clips directory if it doesn't exist
        if not os.path.exists(CLIPS_DIR):
            os.makedirs(CLIPS_DIR)
            logger.info(f"Created directory: {CLIPS_DIR}")

        motion_detected = detect_motion()
        # 1) Check for motion
        if motion_detected:
            logger.info("Motion Detected")

            # 2) record a video and upload to s3
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            video_filename = f"{CLIPS_DIR}/motion_{timestamp}.mp4"

            logger.info(f"Creating video: {video_filename}")
            record_clip(video_filename, 5, camera)
            logger.info("Finished recording video.")

            # 4) Upload video to s3 bucket
            timestamp = str(datetime.now())
            # Fixed: Use the filename as the S3 key, not just "clips"
            s3_key = f"clips/motion_{timestamp}.mp4"
            s3_url = upload_to_s3(video_filename, s3_key)

            # 5) Send notification to MQTT broker  
            if s3_url:
                logger.info("Sending notification")
                send_notification(s3_url, timestamp)
                logger.info("Notification sent")
            else:
                logger.error("Failed to upload video, notification not sent")
    
    finally:
        # Make sure to release the camera
        camera.release()
        logger.info("Camera released")

if __name__ == "__main__":
    main()
