"""
Live streaming functionality for the IoT security camera system.
Provides a Flask-based web interface for streaming camera feed.
"""
import os
import time
import threading
import numpy as np
import cv2
from datetime import datetime
from flask import Flask, Response, render_template
from utils.logger import logger

class LiveStreamServer:
    """Flask-based live streaming server for the IoT security camera system."""
    
    def __init__(self, port=8080):
        """Initialize the live streaming server.
        
        Args:
            port: Port number for the Flask server (default: 8080)
        """
        self.port = port
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Streaming variables
        self.output_frame = None
        self.stream_lock = threading.Lock()
        self.stream_enabled = True
        self.camera = None
        self.privacy_enabled = False
        self.recording = False
        
        # Create templates directory and index.html
        self.create_templates()
        
        # Flask server thread
        self.server_thread = None
        self.stream_thread = None
    
    def setup_routes(self):
        """Set up Flask routes."""
        # Route for home page
        @self.app.route('/')
        def index():
            return render_template('index.html')
            
        # Route for video feed
        @self.app.route('/video_feed')
        def video_feed():
            return Response(self.generate_frames(),
                          mimetype='multipart/x-mixed-replace; boundary=frame')
    
    def create_templates(self):
        """Create the templates directory and index.html file."""
        templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
        
        index_path = os.path.join(templates_dir, "index.html")
        if not os.path.exists(index_path):
            with open(index_path, "w") as f:
                f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Security Camera Stream</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        
        h1 {
            color: #333;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }
        
        .video-container {
            margin: 20px 0;
            position: relative;
        }
        
        .stream {
            width: 100%;
            max-width: 640px;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        .status {
            margin-top: 10px;
            padding: 8px;
            background-color: #f9f9f9;
            border-radius: 4px;
            font-size: 14px;
            color: #666;
        }
        
        .controls {
            margin-top: 20px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
        
        button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 8px 16px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        
        button:hover {
            background-color: #45a049;
        }
        
        footer {
            margin-top: 20px;
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="video-container">
            <img class="stream" src="{{ url_for('video_feed') }}" alt="Video Stream">
            <div class="status">
                Live Stream - <span id="current-time"></span>
            </div>
        </div>
    </div>
    
    <script>
        // Update the current time display
        function updateTime() {
            const timeElement = document.getElementById('current-time');
            const now = new Date();
            timeElement.textContent = now.toLocaleTimeString();
        }
        
        // Update time every second
        setInterval(updateTime, 1000);
        updateTime();
        
        // Function to toggle fullscreen mode
        function toggleFullscreen() {
            const videoElement = document.querySelector('.stream');
            
            if (!document.fullscreenElement) {
                if (videoElement.requestFullscreen) {
                    videoElement.requestFullscreen();
                } else if (videoElement.webkitRequestFullscreen) {
                    videoElement.webkitRequestFullscreen();
                } else if (videoElement.msRequestFullscreen) {
                    videoElement.msRequestFullscreen();
                }
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
            }
        }
        
        // Function to refresh the stream by reloading the image with a new timestamp
        function refreshStream() {
            const streamImg = document.querySelector('.stream');
            const currentSrc = streamImg.src.split('?')[0];
            streamImg.src = currentSrc + '?t=' + new Date().getTime();
        }
    </script>
</body>
</html>
                """)
            logger.info("Created index.html template file.")
    
    def generate_frames(self):
        """Generate frames for the video feed."""
        while True:
            # Wait until the lock is acquired
            #print(self.stream_lock)
            #print("Privacy enabled:")
            #print(self.privacy_enabled)
            #print("Stream enabled:")
            #print(self.stream_enabled)
            #print("Camera:")
            #print(self.camera)
            
            with self.stream_lock:
                # Check if streaming is enabled and the output frame is available
                if (self.privacy_enabled or 
                    not self.stream_enabled or 
                    self.output_frame is None or 
                    self.camera is None):
                    
                    # Create appropriate message based on state
                    if self.privacy_enabled:
                        message = "Privacy Mode Active"
                    elif self.recording:
                        message = "Recording in progress..."
                    else:
                        message = "Camera initializing..."
                    
                    # Create a blank frame with status message
                    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(
                        dummy_frame, 
                        message, 
                        (50, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, 
                        (255, 255, 255), 
                        2
                    )
                    (flag, encoded_image) = cv2.imencode(".jpg", dummy_frame)
                else:
                    # Encode the frame in JPEG format
                    (flag, encoded_image) = cv2.imencode(".jpg", self.output_frame)
                
                # Ensure the frame was successfully encoded
                if not flag:
                    continue
            
            # Yield the output frame in the byte format
            yield(b'--frame\r\n' 
                  b'Content-Type: image/jpeg\r\n\r\n' + 
                  bytearray(encoded_image) + b'\r\n')
            
            # Add a small delay to control frame rate and CPU usage
            time.sleep(0.03)  # Approximately 30 FPS
    
    def stream_capture_thread(self):
        """Thread function to capture frames for streaming."""
        logger.info("Streaming capture thread started")
        
        while True:
            # Only capture if streaming is enabled, privacy mode is off, and camera is initialized
            with self.stream_lock:
                if (self.stream_enabled and 
                    not self.privacy_enabled and 
                    self.camera is not None):
                    try:
                        # Capture a frame from the camera
                        frame = self.camera.capture_array()
                        
                        # Convert the frame from RGB to BGR (OpenCV format)
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        
                        # Optional: Add timestamp to the frame
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        cv2.putText(
                            frame, 
                            current_time, 
                            (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.8, 
                            (255, 255, 255), 
                            2, 
                            cv2.LINE_AA
                        )
                        
                        # Update the global frame that will be sent to clients
                        self.output_frame = frame.copy()
                    except Exception as e:
                        logger.error(f"Error capturing frame for stream: {e}")
            
            # Control the capture rate
            time.sleep(0.03)  # ~30 FPS
    
    def start_server(self):
        """Start the Flask server and streaming thread."""
        # Start the streaming capture thread
        self.stream_thread = threading.Thread(target=self.stream_capture_thread, daemon=True)
        self.stream_thread.start()
        
        # Start the Flask web server
        logger.info(f"Starting streaming server on http://0.0.0.0:{self.port}/")
        self.server_thread = threading.Thread(
            target=lambda: self.app.run(
                host='0.0.0.0', 
                port=self.port, 
                debug=False, 
                threaded=True, 
                use_reloader=False
            ),
            daemon=True
        )
        self.server_thread.start()
    
    def set_camera(self, camera):
        """Set the camera instance for streaming.
        
        Args:
            camera: Picamera2 instance
        """
        with self.stream_lock:
            self.camera = camera
    
    def set_privacy_mode(self, enabled):
        """Set the privacy mode state.
        
        Args:
            enabled: True to enable privacy mode, False to disable
        """
        with self.stream_lock:
            self.privacy_enabled = enabled
    
    def set_recording(self, recording):
        """Set the recording state.
        
        Args:
            recording: True if recording, False otherwise
        """
        with self.stream_lock:
            self.recording = recording
    
    def enable_streaming(self, enabled=True):
        """Enable or disable streaming.
        
        Args:
            enabled: True to enable streaming, False to disable
        """
        with self.stream_lock:
            self.stream_enabled = enabled
