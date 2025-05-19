"""
File utility functions for the IoT security camera system.
"""
import os
import cv2
from datetime import datetime
from utils.logger import logger

def ensure_dirs_exist(directories):
    """Ensure that the specified directories exist, creating them if necessary.
    
    Args:
        directories: List of directory paths to check/create
    """
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")

def extract_frames_from_video(video_path, frames_dir, timestamp, num_frames=3):
    """Extract frames from a video file.
    
    Args:
        video_path: Path to the video file
        frames_dir: Directory to save extracted frames
        timestamp: Timestamp to use in frame filenames
        num_frames: Number of frames to extract
        
    Returns:
        List of extracted frame filenames
    """
    # Create frames directory if it doesn't exist
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    
    try:
        # Open the video file
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            logger.error(f"Error: Could not open video file: {video_path}")
            return []
        
        # Get video properties
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        
        logger.info(f"Video properties: {total_frames} frames, {fps} fps, {duration:.2f} seconds")
        
        # Calculate frame positions to extract (beginning, middle, end)
        if total_frames < 3:
            logger.warning(f"Warning: Video has fewer than 3 frames ({total_frames})")
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
                logger.info(f"Extracted frame {i} (position {frame_pos}) to {frame_filename}")
            else:
                logger.error(f"Error: Could not read frame at position {frame_pos}")
        
        # Release the video
        video.release()
        
        return frame_filenames
    except Exception as e:
        logger.error(f"Error extracting frames: {e}")
        return []

def generate_timestamp():
    """Generate a timestamp for filenames.
    
    Returns:
        tuple: (filename_timestamp, iso_timestamp)
    """
    now = datetime.now()
    filename_timestamp = now.strftime("%Y%m%d_%H%M%S")
    iso_timestamp = now.isoformat()
    return filename_timestamp, iso_timestamp
