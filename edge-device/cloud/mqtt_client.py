"""
MQTT client for the IoT security camera system.
"""
import json
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
from utils.logger import logger

class MQTTClient:
    """MQTT client for AWS IoT communication."""
    def __init__(self, endpoint, client_id, cert_path, private_key_path, root_ca_path):
        """Initialize the MQTT client.
        
        Args:
            endpoint: AWS IoT endpoint
            client_id: Client ID for MQTT connection
            cert_path: Path to certificate file
            private_key_path: Path to private key file
            root_ca_path: Path to Amazon Root CA file
        """
        self.endpoint = endpoint
        self.client_id = client_id
        self.cert_path = cert_path
        self.private_key_path = private_key_path
        self.root_ca_path = root_ca_path
        self.connection = None
        
    def connect(self):
        """Connect to AWS IoT Core.
        
        Returns:
            bool: True if connection was successful, False otherwise
        """
        try:
            # Spin up resources
            event_loop_group = io.EventLoopGroup(1)
            host_resolver = io.DefaultHostResolver(event_loop_group)
            client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
            
            self.connection = mqtt_connection_builder.mtls_from_path(
                endpoint=self.endpoint,
                cert_filepath=self.cert_path,
                pri_key_filepath=self.private_key_path,
                client_bootstrap=client_bootstrap,
                ca_filepath=self.root_ca_path,
                client_id=self.client_id,
                clean_session=False,
                keep_alive_secs=30
            )
            
            logger.info(f"Connecting to {self.endpoint} with client ID '{self.client_id}'...")
            connect_future = self.connection.connect()
            connect_future.result()
            logger.info("MQTT connection established successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to MQTT: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from AWS IoT Core."""
        if self.connection:
            try:
                disconnect_future = self.connection.disconnect()
                disconnect_future.result()
                logger.info("MQTT disconnected")
            except Exception as e:
                logger.error(f"Error disconnecting from MQTT: {e}")
                
    def publish(self, topic, payload, qos=mqtt.QoS.AT_LEAST_ONCE):
        """Publish a message to an MQTT topic.
        
        Args:
            topic: MQTT topic to publish to
            payload: Message payload (dict will be converted to JSON)
            qos: Quality of Service level
            
        Returns:
            bool: True if publishing was successful, False otherwise
        """
        try:
            if not self.connection:
                logger.error("Cannot publish: MQTT not connected")
                return False
                
            # Convert dict payloads to JSON
            if isinstance(payload, dict):
                payload = json.dumps(payload)
                
            self.connection.publish(
                topic=topic,
                payload=payload,
                qos=qos
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            return False
            
    def subscribe(self, topic, callback, qos=mqtt.QoS.AT_LEAST_ONCE):
        """Subscribe to an MQTT topic.
        
        Args:
            topic: MQTT topic to subscribe to
            callback: Callback function for received messages
            qos: Quality of Service level
            
        Returns:
            bool: True if subscription was successful, False otherwise
        """
        try:
            if not self.connection:
                logger.error("Cannot subscribe: MQTT not connected")
                return False
                
            logger.info(f"Subscribing to {topic}")
            subscribe_future, packet_id = self.connection.subscribe(
                topic=topic,
                qos=qos,
                callback=callback
            )
            
            subscribe_result = subscribe_future.result()
            logger.info(f"Subscribed to {topic} with {subscribe_result['qos']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to subscribe to {topic}: {e}")
            return False
