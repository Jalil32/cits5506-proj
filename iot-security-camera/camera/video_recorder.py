"""
Video recorder for the IoT security camera system.
"""
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from time import sleep
from utils.logger import logger

class VideoRecorder:
    """Records video using the Pi camera."""
    
    @staticmethod
    def record_video(camera, video_filename, duration):
        """Record a video clip directly to MP4 format.
        
        Args:
            camera: Picamera2 instance
            video_filename: Output video filename
            duration: Recording duration in seconds
            
        Returns:
            str or None: Path to the recorded video if successful, None otherwise
        """
        try:
            if camera is None:
                logger.error("Cannot record video: Camera is not initialized")
                return None
                
            encoder = H264Encoder(bitrate=10000000)
            camera.start_recording(encoder, FfmpegOutput(video_filename))
            logger.info(f'Started recording to {video_filename}')

            sleep(duration)
            camera.stop_recording()

            logger.info('Finished recording')
            return video_filename
                
        except Exception as e:
            logger.error(f"Error during video recording: {e}")
            
            # Try to stop recording if an error occurred mid-recording
            try:
                camera.stop_recording()
            except:
                pass
                
            return None
