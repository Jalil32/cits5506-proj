"""
Utils module initialization
"""

from utils.logger import logger, setup_logger
from utils.file_utils import extract_frames_from_video, ensure_dirs_exist, generate_timestamp

__all__ = ['logger', 'setup_logger', 'extract_frames_from_video', 'ensure_dirs_exist', 'generate_timestamp']
