"""
Main entry point for the IoT security camera system.
"""
import os
import time
import threading

# Import configuration
import config

# Import modules
from utils import logger, ensure_dirs_exist
from cloud import MQTTClient, S3Client
from camera import CameraManager, VideoRecorder
from motion import MotionDetector
from privacy import PrivacyManager
from streaming import LiveStreamManager

import os

def main():
    """Main function for the IoT security camera system."""
    try:

        logger.info("Starting IoT security camera system...")
        # Main loop variables
        camera_initialized = False
        detector_initialized = False
        detector = None
        
        # Create required directories
        ensure_dirs_exist([config.CLIPS_DIR, config.FRAMES_DIR])
        
        # Initialize MQTT client
        mqtt_client = MQTTClient(
            endpoint=config.ENDPOINT,
            client_id=config.CLIENT_ID,
            cert_path=config.PATH_TO_CERTIFICATE,
            private_key_path=config.PATH_TO_PRIVATE_KEY,
            root_ca_path=config.PATH_TO_AMAZON_ROOT_CA_1
        )
        
        # Connect to MQTT
        if not mqtt_client.connect():
            logger.error("Failed to connect to MQTT. Exiting...")
            return
            
        # Initialize S3 client
        s3_client = S3Client(bucket_name=config.S3_BUCKET)
        
        # Initialize privacy manager
        privacy_manager = PrivacyManager(
            mqtt_client=mqtt_client,
            privacy_state_file=config.PRIVACY_STATE_FILE,
            status_topic=config.PRIVACY_STATUS_TOPIC,
            client_id=config.CLIENT_ID
        )
        
        # Subscribe to privacy commands
        mqtt_client.subscribe(
            topic=config.PRIVACY_COMMAND_TOPIC,
            callback=privacy_manager.handle_privacy_command
        )
        
        # Start privacy status heartbeat
        privacy_manager.start_status_heartbeat()
        
        # Initialize camera manager
        camera_manager = CameraManager()

        # Initialize camera if needed
        if not camera_initialized:
            camera_initialized = camera_manager.initialize()
            if not camera_initialized:
                time.sleep(5)  # Wait before retrying
        
        # Initialize live stream manager
        live_stream_manager = LiveStreamManager(
            camera_manager=camera_manager,
            mqtt_client=mqtt_client,
            command_topic=config.STREAM_COMMAND_TOPIC,
            status_topic=config.STREAM_STATUS_TOPIC,
            client_id=config.CLIENT_ID
        )
        
        logger.info("Starting main detection loop. Press CTRL+C to exit.")
        
        while True:
            # Check privacy state
            if privacy_manager.is_privacy_enabled():
                # If privacy mode enabled, terminate live stream
                if live_stream_manager.streaming:
                    live_stream_manager.set_privacy_mode(True)
                    live_stream_manager.set_recording(False)
                    live_stream_manager.stop_stream()

                # If privacy mode is enabled, make sure camera is off
                if camera_initialized:
                    logger.info("Privacy mode active, shutting down camera")
                    camera_manager.shutdown()
                    camera_initialized = False
                
                # If detector is initialized, shut it down
                if detector_initialized and detector:
                    logger.info("Privacy mode active, shutting down detector")
                    detector_initialized = False
                    detector = None
                
                privacy_manager.set_detection_running(False)
                time.sleep(1)  # Reduced CPU usage in privacy mode
                continue
            
            # Initialize camera if needed
            if not camera_initialized:
                camera_initialized = camera_manager.initialize()
                if not camera_initialized:
                    time.sleep(5)  # Wait before retrying
                    continue

            if not live_stream_manager.streaming:
                # Start the stream
                live_stream_manager.set_privacy_mode(False)
                live_stream_manager.set_recording(True)
                live_stream_manager.start_stream()
            
            # Initialize detector if needed
            if not detector_initialized:
                try:
                    logger.info("Initializing motion detector...")
                    # Create MotionDetector instance with custom thresholds
                    detector = MotionDetector(
                        baud_rate=config.MOTION_BAUD_RATE,
                        speed_threshold=config.MOTION_SPEED_THRESHOLD,
                        range_threshold=config.MOTION_RANGE_THRESHOLD,
                        energy_threshold=config.MOTION_ENERGY_THRESHOLD,
                    )
                    
                    # Initialize the detector
                    if detector.initialize():
                        detector_initialized = True
                        logger.info("Motion detector initialized successfully")
                    else:
                        logger.error("Failed to initialize detector")
                        time.sleep(5)  # Wait before retrying
                        continue
                except Exception as e:
                    logger.error(f"Failed to initialize detector: {e}")
                    time.sleep(5)  # Wait before retrying
                    continue
            
                            # Both camera and detector are initialized, run detection loop
            try:
                # Add tracking for periodic sensor flushing
                last_sensor_flush = time.time()
                sensor_flush_interval = 5  # Flush sensor every 5 seconds
                
                motion_detected, data = detector.detect_motion(debug=True)
                
                # Current time for flush calculations
                current_time = time.time()
                
                # Periodically flush sensor readings to avoid stuck values
                if current_time - last_sensor_flush >= sensor_flush_interval:
                    detector.flush_sensor_readings()
                    last_sensor_flush = current_time
                    
                # Act on motion detection
                if motion_detected:

                    # Stop the stream
                    print("Motion detected, stopping stream")
                    live_stream_manager.set_recording(True)
                    live_stream_manager.stop_stream()

                    privacy_manager.set_detection_running(True)
                    logger.info("Motion detected! Taking action...")
                    logger.info(f"Motion data: Speed={data.get('target_speed', 'N/A')}, Range={data.get('target_range', 'N/A')}, Energy={data.get('target_energy', 'N/A')}")
                    
                    # Process the motion detection event
                    process_motion_detection(
                        camera_manager=camera_manager,
                        s3_client=s3_client,
                        mqtt_client=mqtt_client
                    )
                        
                    logger.info("Motion detection flow finished. Sleeping now.")
                    privacy_manager.set_detection_running(False)
                    
                    for i in range(50):
                        motion_detected, data = detector.detect_motion()
                    
                    # This prevents any possibility of repeated detections
                    # Start the stream
                    print("Reinitialising camera and starting stream")
                    camera_initialized = camera_manager.initialize()
                    live_stream_manager.set_recording(False)
                    live_stream_manager.start_stream()

                    time.sleep(config.MOTION_DETECTION_COOLDOWN)
                        
                    logger.info("Cooldown period complete")
                
                else:
                    # No motion detected, short sleep to avoid CPU overuse
                    time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in detection loop: {e}")
                time.sleep(1)  # Brief pause before continuing
    
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Shutting down...")
    
    finally:
        # Cleanup
        try:
            # Shutdown camera if initialized
            if 'camera_manager' in locals() and camera_manager:
                camera_manager.shutdown()
                
            # Disconnect MQTT if connected
            if 'mqtt_client' in locals() and mqtt_client:
                mqtt_client.disconnect()
                
            logger.info("Cleanup complete. Exiting...")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


def process_motion_detection(camera_manager, s3_client, mqtt_client):
    """Process a motion detection event.
    
    Args:
        camera_manager: CameraManager instance
        s3_client: S3Client instance
        mqtt_client: MQTTClient instance
    """
    from utils import generate_timestamp, extract_frames_from_video
    import os
    
    # Create timestamps for filenames
    filename_timestamp, iso_timestamp = generate_timestamp()
    
    # Define paths
    video_filename = f"{config.CLIPS_DIR}/motion_{filename_timestamp}.mp4"
    frames_subdir = os.path.join(config.FRAMES_DIR, filename_timestamp)
    
    # Record the video
    logger.info(f"Recording video: {video_filename}")
    camera = camera_manager.get_camera()
    recorded_video = VideoRecorder.record_video(
        camera=camera,
        video_filename=video_filename,
        duration=config.RECORDING_DURATION
    )
    
    if not recorded_video:
        logger.error("Failed to record video, skipping this detection")
        return
    
    # Try to extract frames from the recorded video
    logger.info("Attempting to extract frames from the recorded video")
    frame_files = extract_frames_from_video(
        video_path=video_filename,
        frames_dir=frames_subdir,
        timestamp=filename_timestamp,
        num_frames=config.FRAMES_TO_EXTRACT
    )
    
    # If no frames were extracted, capture them directly
    if not frame_files:
        logger.info("No frames extracted from video, capturing directly from camera")
        frame_files = camera_manager.capture_frames(
            frames_dir=frames_subdir,
            timestamp=filename_timestamp,
            num_frames=config.FRAMES_TO_EXTRACT
        )
        
    if not frame_files:
        logger.warning("No frames were captured")
    else:
        logger.info(f"Successfully captured {len(frame_files)} frames")
    
    # Upload video to S3
    video_s3_key = f"clips/motion_{filename_timestamp}.mp4"
    video_s3_url = s3_client.upload_file(video_filename, video_s3_key)
    
    # Upload frames to S3
    frame_s3_urls = []
    for i, frame_file in enumerate(frame_files):
        frame_s3_key = f"frames/{filename_timestamp}/frame_{i}.jpg"
        frame_s3_url = s3_client.upload_file(frame_file, frame_s3_key)
        if frame_s3_url:
            frame_s3_urls.append(frame_s3_url)
    
    # Send notification to MQTT broker with both video and frame URLs  
    if video_s3_url and frame_s3_urls:
        message = {
            "device_id": config.CLIENT_ID,
            "alert": "Motion detected",
            "timestamp": iso_timestamp,
            "video_url": video_s3_url,
            "frame_urls": frame_s3_urls
        }
        
        mqtt_client.publish(topic=config.TOPIC_ALERT, payload=message)
        logger.info("Notification sent with video and frame URLs")
    else:
        logger.error("Failed to upload media, notification not sent")


if __name__ == "__main__":
    main()
