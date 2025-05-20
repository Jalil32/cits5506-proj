"""
Logger utility for the IoT security camera system.
"""
import logging

def setup_logger(log_level=logging.INFO):
    """Set up and configure application logger.
    
    Args:
        log_level: The logging level to use
        
    Returns:
        logger: Configured logger instance
    """
    # Create a logger
    logger = logging.getLogger('iot_security_camera')
    logger.setLevel(log_level)
    
    # Avoid adding duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
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

# Create a default logger instance
logger = setup_logger()
