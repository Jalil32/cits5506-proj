"""
Live stream manager for the IoT security camera system.
"""
import json
import threading
from datetime import datetime
from utils.logger import logger
from awscrt import mqtt
from streaming.live_stream_server import LiveStreamServer

class LiveStreamManager:
    """Manages live streaming functionality."""
    
    def __init__(self, camera_manager, mqtt_client, command_topic, status_topic, client_id, stream_port=8080):
        """Initialize the live stream manager.
        
        Args:
            camera_manager: Camera manager instance
            mqtt_client: MQTT client instance
            command_topic: Topic for stream commands
            status_topic: Topic for stream status updates
            client_id: Device client ID
            stream_port: Port for the streaming server
        """
        self.camera_manager = camera_manager
        self.mqtt_client = mqtt_client
        self.command_topic = command_topic
        self.status_topic = status_topic
        self.client_id = client_id
        self.streaming = False
        
        # Create the streaming server
        self.stream_server = LiveStreamServer(port=stream_port)
        
        # Start the streaming server
        self.stream_server.start_server()

        # Start the stream
        self.start_stream()
        
        # Subscribe to commands
        mqtt_client.subscribe(
            topic=self.command_topic,
            callback=self.handle_stream_command
        )
        
        logger.info(f"LiveStreamManager initialized and subscribed to {command_topic}")
        logger.info(f"Streaming server available at http://0.0.0.0:{stream_port}/")
    
    def handle_stream_command(self, topic, payload, dup, qos, retain, **kwargs):
        """Handle stream command MQTT messages.
        
        Args:
            topic: MQTT topic
            payload: Message payload
            dup: Whether message is a duplicate
            qos: Quality of Service level
            retain: Whether message is retained
            **kwargs: Additional arguments
        """
        try:
            payload_data = json.loads(payload.decode('utf-8'))
            stream_enabled = payload_data.get("streamEnabled", False)
            
            logger.info(f"Received stream command: streamEnabled={stream_enabled}")
            
            if stream_enabled and not self.streaming:
                self.start_stream()
            elif not stream_enabled and self.streaming:
                self.stop_stream()
                
            self.publish_status()
        except Exception as e:
            logger.error(f"Error handling stream command: {e}")
    
    def start_stream(self):
        """Start the live stream."""
        # Update camera reference in the stream server
        camera = self.camera_manager.get_camera()
        self.stream_server.set_camera(camera)
        self.stream_server.enable_streaming(True)
        self.streaming = True
        logger.info("Live stream started")
        
    def stop_stream(self):
        """Stop the live stream."""
        self.stream_server.enable_streaming(False)
        self.streaming = False
        logger.info("Live stream stopped")
    
    def set_privacy_mode(self, enabled):
        """Set privacy mode state for streaming.
        
        Args:
            enabled: True to enable privacy mode, False to disable
        """
        self.stream_server.set_privacy_mode(enabled)
        
    def set_recording(self, recording):
        """Set recording state for streaming.
        
        Args:
            recording: True if recording is in progress, False otherwise
        """
        self.stream_server.set_recording(recording)
    
    def publish_status(self):
        """Publish current streaming status to MQTT."""
        status = {
            "streaming": self.streaming,
            "deviceId": self.client_id,
            "timestamp": datetime.now().isoformat()
        }
        
        self.mqtt_client.publish(
            topic=self.status_topic,
            payload=json.dumps(status)
        )
