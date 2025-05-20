"""
Camera manager for the IoT security camera system.
"""
import time
import cv2
from picamera2 import Picamera2
from utils.logger import logger

class CameraManager:
    """Manages the Raspberry Pi camera initialization and capture."""
    
    def __init__(self):
        """Initialize camera manager."""
        self.camera = None
        
    def initialize(self):
        """Initialize and configure the Pi camera.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        try:
            logger.info("Initializing Pi camera...")
            
            # First, make sure any existing camera instance is properly closed
            if self.camera is not None:
                try:
                    self.camera.stop()
                    self.camera.close()
                    self.camera = None
                    time.sleep(1)  # Give camera time to fully release
                except Exception as e:
                    logger.warning(f"Error closing existing camera: {e}")

            # Create a new camera instance
            self.camera = Picamera2()
            
            # Create configurations
            video_config = self.camera.create_video_configuration()
            preview_config = self.camera.create_preview_configuration(main={"size": (640, 480)})
            
            # Configure and start the camera
            self.camera.configure(video_config)
            time.sleep(0.5)  # Short pause between operations
            
            # Start the camera
            self.camera.start()
            
            # Allow camera to warm up
            time.sleep(2)
            
            logger.info("Pi camera initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            
            # If we failed, make sure to clean up
            if self.camera is not None:
                try:
                    self.camera.close()
                except:
                    pass
                self.camera = None
            
            return False
            
    def shutdown(self):
        """Safely shut down the camera."""
        if self.camera is not None:
            try:
                logger.info("Shutting down camera...")
                self.camera.stop()
                self.camera.close()
                self.camera = None
                logger.info("Camera shut down successfully")
            except Exception as e:
                logger.error(f"Error shutting down camera: {e}")
                
    def get_camera(self):
        """Get the camera instance.
        
        Returns:
            Picamera2 or None: Camera instance if initialized, None otherwise
        """
        return self.camera
                
    def capture_frames(self, frames_dir, timestamp, num_frames=3):
        """Capture frames directly from the camera.
        
        Args:
            frames_dir: Directory to save captured frames
            timestamp: Timestamp to use in frame filenames
            num_frames: Number of frames to capture
            
        Returns:
            list: List of captured frame filenames
        """
        import os
        
        # Create frames directory if it doesn't exist
        if not os.path.exists(frames_dir):
            os.makedirs(frames_dir)
        
        frame_filenames = []
        
        try:
            if not self.camera:
                logger.error("Cannot capture frames: Camera not initialized")
                return []
                
            logger.info(f"Capturing {num_frames} frames directly from camera...")
            
            # Capture frames with a small delay between them
            for i in range(num_frames):
                # Capture a frame
                frame = self.camera.capture_array()
                
                # Save the frame
                frame_filename = os.path.join(frames_dir, f"frame_{timestamp}_{i}.jpg")
                cv2.imwrite(frame_filename, frame)
                frame_filenames.append(frame_filename)
                logger.info(f"Captured and saved frame {i} to {frame_filename}")
                
                # Small delay between frames
                time.sleep(0.5)
                
            return frame_filenames
        except Exception as e:
            logger.error(f"Error capturing frames directly: {e}")
            return []
