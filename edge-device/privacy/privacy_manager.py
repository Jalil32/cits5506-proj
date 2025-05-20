"""
Privacy mode management for the IoT security camera system.
"""
import json
import os
import threading
from enum import Enum
from datetime import datetime
from utils.logger import logger

class PrivacyState(Enum):
    """Enum representing the privacy mode states."""
    DISABLED = 0  # Normal operation - detection and recording active
    ENABLED = 1   # Privacy mode - detection and recording paused

class PrivacyManager:
    """Manages privacy mode for the camera system."""
    
    def __init__(self, mqtt_client, privacy_state_file, status_topic, client_id):
        """Initialize the privacy manager.
        
        Args:
            mqtt_client: MQTT client for communication
            privacy_state_file: File path to persist privacy state
            status_topic: MQTT topic for publishing status updates
            client_id: Device client ID
        """
        self.mqtt_client = mqtt_client
        self.privacy_state_file = privacy_state_file
        self.status_topic = status_topic
        self.client_id = client_id
        self.privacy_state = PrivacyState.DISABLED
        self.detection_running = False
        self.privacy_lock = threading.Lock()
        
        # Load initial state
        self.load_privacy_state()
        
    def load_privacy_state(self):
        """Load privacy state from file if it exists."""
        try:
            if os.path.exists(self.privacy_state_file):
                with open(self.privacy_state_file, 'r') as f:
                    state_data = json.load(f)
                    self.privacy_state = PrivacyState.ENABLED if state_data.get("privacy_enabled", False) else PrivacyState.DISABLED
                    logger.info(f"Loaded privacy state: {self.privacy_state}")
            else:
                logger.info(f"No saved privacy state found, using default: {self.privacy_state}")
        except Exception as e:
            logger.error(f"Error loading privacy state: {e}")
    
    def save_privacy_state(self):
        """Save privacy state to file."""
        try:
            with open(self.privacy_state_file, 'w') as f:
                state_data = {"privacy_enabled": self.privacy_state == PrivacyState.ENABLED}
                json.dump(state_data, f)
                logger.info(f"Saved privacy state: {self.privacy_state}")
        except Exception as e:
            logger.error(f"Error saving privacy state: {e}")
            
    def handle_privacy_command(self, topic, payload, dup, qos, retain, **kwargs):
        """Handle privacy mode command messages.
        
        Args:
            topic: MQTT topic
            payload: Message payload
            dup: Whether message is a duplicate
            qos: Quality of Service level
            retain: Whether message is retained
            **kwargs: Additional arguments
        """
        try:
            # Parse the JSON message
            payload_data = json.loads(payload.decode('utf-8'))
            logger.info(f"Received privacy command on topic {topic}: {payload_data}")
            
            # Extract the privacy mode state from the message
            new_privacy_enabled = payload_data.get("privacyModeEnabled", False)
            
            with self.privacy_lock:
                # Update state based on command
                if new_privacy_enabled and self.privacy_state == PrivacyState.DISABLED:
                    # Enable privacy mode
                    self.privacy_state = PrivacyState.ENABLED
                    logger.info("Privacy mode enabled")
                    self.save_privacy_state()
                elif not new_privacy_enabled and self.privacy_state == PrivacyState.ENABLED:
                    # Disable privacy mode
                    self.privacy_state = PrivacyState.DISABLED
                    logger.info("Privacy mode disabled")
                    self.save_privacy_state()
                    
                # Publish current status
                self.publish_status()
            
        except json.JSONDecodeError:
            logger.error(f"Failed to parse privacy command: Invalid JSON - {payload}")
        except Exception as e:
            logger.error(f"Error handling privacy command: {str(e)}")
    
    def publish_status(self):
        """Publish current privacy and recording status to MQTT."""
        status_payload = {
            "privacyModeEnabled": self.privacy_state == PrivacyState.ENABLED,
            "deviceId": self.client_id,
            "lastStateChange": datetime.now().isoformat(),
            "isRecording": self.detection_running
        }
        
        self.mqtt_client.publish(
            topic=self.status_topic,
            payload=json.dumps(status_payload)
        )
        logger.info(f"Published status: {status_payload}")
    
    def start_status_heartbeat(self, interval=60):
        """Start a thread to periodically publish status.
        
        Args:
            interval: Status update interval in seconds
        """
        def heartbeat_worker():
            while True:
                self.publish_status()
                threading.Event().wait(interval)  # More reliable than sleep for long intervals
                
        heartbeat_thread = threading.Thread(target=heartbeat_worker, daemon=True)
        heartbeat_thread.start()
        logger.info(f"Started privacy status heartbeat (interval: {interval}s)")
        
    def set_detection_running(self, is_running):
        """Update the detection running status.
        
        Args:
            is_running: Whether detection/recording is currently running
        """
        with self.privacy_lock:
            self.detection_running = is_running
            
    def is_privacy_enabled(self):
        """Check if privacy mode is currently enabled.
        
        Returns:
            bool: True if privacy mode is enabled, False otherwise
        """
        with self.privacy_lock:
            return self.privacy_state == PrivacyState.ENABLED
