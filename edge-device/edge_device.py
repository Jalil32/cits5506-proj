import boto3
from awscrt import io, mqtt 
from awsiot import mqtt_connection_builder 
import os 
import time
import json
import logging
from datetime import datetime
import cv2
from picamera2 import Picamera2
from motion_detector import *
from picamera2 import *
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from time import sleep

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

# Local storage directories
CLIPS_DIR = "clips"
FRAMES_DIR = "frames"

# Fixed S3 bucket name - removed "s3://" prefix and trailing slash
S3_BUCKET = "jalil-iot-project"

# Number of frames to extract per video
FRAMES_TO_EXTRACT = 3

DURATION = 20


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
    """Set up and configure a basic logger."""
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

def capture_frames_directly(picam, frames_dir, timestamp, num_frames=3):
    """
    Capture frames directly from the camera instead of extracting from video
    Returns a list of captured frame filenames
    """
    # Create frames directory if it doesn't exist
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    
    frame_filenames = []
    
    try:
        print(f"Capturing {num_frames} frames directly from camera...")
        
        # Capture frames with a small delay between them
        for i in range(num_frames):
            # Capture a frame
            frame = picam.capture_array()
            
            # Save the frame
            frame_filename = os.path.join(frames_dir, f"frame_{timestamp}_{i}.jpg")
            cv2.imwrite(frame_filename, frame)
            frame_filenames.append(frame_filename)
            print(f"Captured and saved frame {i} to {frame_filename}")
            
            # Small delay between frames
            time.sleep(0.5)
            
        return frame_filenames
    except Exception as e:
        print(f"Error capturing frames directly: {e}")
        return []

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

# Function to send MQTT notification with both video and frames
def send_notification(video_url, frame_urls, timestamp):
    message = {
        "device_id": CLIENT_ID,
        "alert": "Motion detected",
        "timestamp": timestamp,
        "video_url": video_url,
        "frame_urls": frame_urls
    }
    
    mqtt_connection.publish(
        topic=TOPIC,
        payload=json.dumps(message),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )


def record_video(video_filename, duration, camera):
    """Record a video clip directly to MP4 format"""
    try:

        encoder = H264Encoder(bitrate=10000000)

        camera.start_recording(encoder, FfmpegOutput(video_filename))
        print('STARTED RECORDING')

        sleep(duration)
        camera.stop_recording()

        print('FINISHED RECORDING')
        return video_filename
            
    except Exception as e:
        print(f"Error during video recording: {e}")
        return None


def extract_frames_from_video(video_path, frames_dir, timestamp):
    """
    Extract frames from a video file that has already been recorded
    Returns a list of extracted frame filenames
    """
    # Create frames directory if it doesn't exist
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    
    try:
        # Open the video file
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            print(f"Error: Could not open video file: {video_path}")
            # If we can't open the video, we'll capture frames directly
            return []
        
        # Get video properties
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        
        print(f"Video properties: {total_frames} frames, {fps} fps, {duration:.2f} seconds")
        
        # Calculate frame positions to extract (beginning, middle, end)
        if total_frames < 3:
            print(f"Warning: Video has fewer than 3 frames ({total_frames})")
            frame_positions = list(range(total_frames))
        else:
            frame_positions = [
                0,                      # Beginning frame
                total_frames // 2,      # Middle frame
                total_frames - 1        # End frame
            ]
        
        frame_filenames = []
        
        # Extract specified frames
        for i, frame_pos in enumerate(frame_positions):
            # Set the position
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            
            # Read the frame
            ret, frame = video.read()
            if ret:
                # Save the frame
                frame_filename = os.path.join(frames_dir, f"frame_{timestamp}_{i}.jpg")
                cv2.imwrite(frame_filename, frame)
                frame_filenames.append(frame_filename)
                print(f"Extracted frame {i} (position {frame_pos}) to {frame_filename}")
            else:
                print(f"Error: Could not read frame at position {frame_pos}")
        
        # Release the video
        video.release()
        
        return frame_filenames
    except Exception as e:
        print(f"Error extracting frames: {e}")
        return []

def main():
    logger = setup_logger()

    # 1) Connect to Raspberry Pi camera    
    logger.info("Initialising Pi camera...")
    camera = Picamera2()

    video_config = camera.create_video_configuration()
    config = camera.create_preview_configuration(main={"size": (640, 480)})
    camera.configure(video_config)
    
    # Configure camera
    camera.configure(config)
    camera.start()
    
    # Allow camera to warm up
    time.sleep(2)
    logger.info("Pi camera initialized successfully")

    # 2) Create MotionDetector instance with custom thresholds
    detector = MotionDetector(
        baud_rate=9600,
        speed_threshold=0.1,  # m/s
        range_threshold=80,   # cm
        energy_threshold=5
    )

    # Initialize the detector
    if not detector.initialize():
        print("Failed to initialize detector. Exiting.")
        return

    try:
        # Create directories if they don't exist
        for directory in [CLIPS_DIR, FRAMES_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Created directory: {directory}")

        print("\nRunning detection loop. Press CTRL+C to exit.\n")
        while True:

            motion_detected, data = detector.detect_motion(debug=True)

            # Will need to add privacy button here
                
            # Act on motion detection
            if motion_detected:
                print("Motion detected! Taking action...")
                # Add your action code here

                # 2) Create a timestamp for filenames
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                iso_timestamp = datetime.now().isoformat()
                
                video_filename = f"{CLIPS_DIR}/motion_{timestamp}.mp4"  # Changed to .avi
                frames_subdir = os.path.join(FRAMES_DIR, timestamp)

                # 3) First, record the video
                logger.info(f"Recording video: {video_filename}")
                recorded_video = record_video(video_filename, DURATION, camera)  # 5 seconds duration
                
                if not recorded_video:
                    logger.error("Failed to record video, aborting")
                    return
                
                # 4) First try to extract frames from the recorded video
                logger.info("Attempting to extract frames from the recorded video")
                frame_files = extract_frames_from_video(video_filename, frames_subdir, timestamp)
                
                # If no frames were extracted, capture them directly
                if not frame_files:
                    logger.info("No frames extracted from video, capturing directly from camera")
                    frame_files = capture_frames_directly(camera, frames_subdir, timestamp, 3)
                    
                if not frame_files:
                    logger.warning("No frames were captured")
                else:
                    logger.info(f"Successfully captured {len(frame_files)} frames")
                
                # 5) Upload video to S3
                video_s3_key = f"clips/motion_{timestamp}.mp4"  # Changed to .avi
                video_s3_url = upload_to_s3(video_filename, video_s3_key)
                
                # 6) Upload frames to S3
                frame_s3_urls = []
                for i, frame_file in enumerate(frame_files):
                    frame_s3_key = f"frames/{timestamp}/frame_{i}.jpg"
                    frame_s3_url = upload_to_s3(frame_file, frame_s3_key)
                    if frame_s3_url:
                        frame_s3_urls.append(frame_s3_url)
                
                ## 7) Send notification to MQTT broker with both video and frame URLs  
                #if video_s3_url and frame_s3_urls:
                #    logger.info("Sending notification with video and frames")
                #    send_notification(video_s3_url, frame_s3_urls, iso_timestamp)
                #    logger.info("Notification sent")
                #else:
                #    logger.error("Failed to upload media, notification not sent")
                    
                logger.info("Motion detection flow finished. Sleeping now.")
                time.sleep(20)
    
    finally:
        # Make sure to stop the camera
        camera.stop()
        logger.info("Camera stopped")

if __name__ == "__main__":
    main()
