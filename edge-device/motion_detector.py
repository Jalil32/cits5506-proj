import sys
import os
import time
import RPi.GPIO as GPIO
from DFRobot_C4001 import *

class MotionDetector:
    """
    A class for detecting motion using the DFRobot C4001 24GHz radar sensor.
    Provides methods for initializing the sensor, configuring detection parameters,
    and detecting motion based on speed, range, and energy thresholds.
    """
    
    def __init__(self, 
                 baud_rate=9600, 
                 speed_threshold=0.1,  # m/s - lowered for subtle hand movements
                 range_threshold=80,   # cm - approximately one arm's length (~30 inches)
                 energy_threshold=5):  # lowered for better sensitivity to small targets like hands
        """
        Initialize the MotionDetector with the specified thresholds.
        
        Args:
            baud_rate (int): Baud rate for the UART connection
            speed_threshold (float): Minimum speed to detect motion (m/s)
            range_threshold (int): Maximum range to detect motion (cm)
            energy_threshold (int): Minimum energy to detect motion
        """
        self.speed_threshold = speed_threshold
        self.range_threshold = range_threshold
        self.energy_threshold = energy_threshold
        
        # Create radar instance
        try:
            self.radar = DFRobot_C4001_UART(baud_rate)
            print(f"Successfully connected at {baud_rate} baud rate")
        except Exception as e:
            print(f"Error creating radar instance: {e}")
            self._print_debug_info()
            raise
        
        # Initialize status
        self.is_initialized = False
        
    def _print_debug_info(self):
        """Print debug information about available items and serial ports"""
        print("\nAvailable items in DFRobot_C4001 module:")
        for item in dir(DFRobot_C4001):
            if not item.startswith("__"):
                print(f"  - {item}")

        print("\nLet's examine what serial ports are available on your system:")
        os.system("ls -l /dev/serial*")
        
    def initialize(self):
        """
        Initialize the radar sensor and configure the detection settings.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        print("Initializing radar sensor...")

        # Initialize the radar
        if not self.radar.begin():
            print("Sensor initialization failed!")
            return False

        print("Sensor initialized successfully")
        
        # Configure sensor settings
        self._configure_sensor()
        
        # Print configuration
        self._print_configuration()
        
        self.is_initialized = True
        return True
        
    def _configure_sensor(self):
        """Configure the sensor mode and detection thresholds"""
        # Set sensor to speed mode
        try:
            if hasattr(self.radar, 'set_sensor_mode'):
                if hasattr(self.radar, 'SPEED_MODE'):
                    self.radar.set_sensor_mode(self.radar.SPEED_MODE)
                else:
                    self.radar.set_sensor_mode(1)  # Typically 1 = speed mode
            else:
                print("Note: set_sensor_mode not available")
        except Exception as e:

            print(f"Warning: Could not set sensor mode: {e}")

        # Set detection thresholds
        try:
            if hasattr(self.radar, 'set_detect_thres'):
                self.radar.set_detect_thres(5, 100, 5)  # min range, max range, threshold
                print("Detection thresholds set")
            else:
                print("Note: set_detect_thres not available")
        except Exception as e:
            print(f"Warning: Could not set detection thresholds: {e}")

        # Set fretting detection if available
        try:
            if hasattr(self.radar, 'set_fretting_detection'):
                if hasattr(self.radar, 'FRETTING_ON'):
                    self.radar.set_fretting_detection(self.radar.FRETTING_ON)
                else:
                    self.radar.set_fretting_detection(1)  # Typically 1 = ON
                print("Fretting detection enabled")
            else:
                print("Note: set_fretting_detection not available")
        except Exception as e:
            print(f"Warning: Could not set fretting detection: {e}")
            
    def _print_configuration(self):
        """Print the current configuration of the radar sensor"""
        print("\nConfiguration:")
        if hasattr(self.radar, 'get_tmin_range'):
            print("min range = " + str(self.radar.get_tmin_range()))
        if hasattr(self.radar, 'get_tmax_range'):
            print("max range = " + str(self.radar.get_tmax_range()))
        if hasattr(self.radar, 'get_thres_range'):
            print("thres range = " + str(self.radar.get_thres_range()))
        if hasattr(self.radar, 'get_fretting_detection'):
            print("fretting detection = " + str(self.radar.get_fretting_detection()))

        print("\nMotion Detection Thresholds:")
        print(f"Speed threshold: {self.speed_threshold} m/s")
        print(f"Range threshold: {self.range_threshold} cm")
        print(f"Energy threshold: {self.energy_threshold}")
        print("Motion will be detected when all parameters exceed these thresholds.\n")
        
    def update_thresholds(self, speed=None, range_val=None, energy=None):
        """
        Update the motion detection thresholds.
        
        Args:
            speed (float, optional): New speed threshold in m/s
            range_val (int, optional): New range threshold in cm
            energy (int, optional): New energy threshold
        """
        if speed is not None:
            self.speed_threshold = speed
        if range_val is not None:
            self.range_threshold = range_val
        if energy is not None:
            self.energy_threshold = energy
        
        print("\nUpdated Motion Detection Thresholds:")
        print(f"Speed threshold: {self.speed_threshold} m/s")
        print(f"Range threshold: {self.range_threshold} cm")
        print(f"Energy threshold: {self.energy_threshold}")
        
    def check_motion_detected(self, speed, range_val, energy, debug=False):
        """
        Check if all parameters exceed thresholds for motion detection.
        
        Args:
            speed (float): Measured speed in m/s
            range_val (float): Measured range in cm
            energy (float): Measured energy
            debug (bool): Whether to print debug information
            
        Returns:
            bool: True if motion is detected, False otherwise
        """
        speed_detected = abs(speed) >= self.speed_threshold
        range_detected = range_val <= self.range_threshold  # Object is within range threshold
        energy_detected = energy >= self.energy_threshold

        # For debugging - print detailed threshold check results
        if debug:
            print(f"Speed check: {abs(speed)} >= {self.speed_threshold} = {speed_detected}")
            print(f"Range check: {range_val} <= {self.range_threshold} = {range_detected}")
            print(f"Energy check: {energy} >= {self.energy_threshold} = {energy_detected}")

        # You can be more lenient by requiring only 2 out of 3 conditions
        # Uncomment the next line and comment the line after if you want that behavior
        # return (speed_detected and range_detected) or (speed_detected and energy_detected) or (range_detected and energy_detected)
        return speed_detected and range_detected and energy_detected
    
    def get_sensor_data(self):
        """
        Get the current sensor data (target number, speed, range, and energy).
        
        Returns:
            dict: Dictionary containing the sensor data
        """
        if not self.is_initialized:
            print("Warning: Sensor not initialized. Call initialize() first.")
            return None
            
        data = {}
        
        # Get target data with error handling for each method
        try:
            data['target_number'] = self.radar.get_target_number() if hasattr(self.radar, 'get_target_number') else 0
        except Exception as e:
            print(f"Warning: Could not get target number: {e}")
            data['target_number'] = 0

        try:
            data['target_speed'] = self.radar.get_target_speed() if hasattr(self.radar, 'get_target_speed') else 0
        except Exception as e:
            print(f"Warning: Could not get target speed: {e}")
            data['target_speed'] = 0

        try:
            data['target_range'] = self.radar.get_target_range() if hasattr(self.radar, 'get_target_range') else 0
        except Exception as e:
            print(f"Warning: Could not get target range: {e}")
            data['target_range'] = 0

        try:
            data['target_energy'] = self.radar.get_target_energy() if hasattr(self.radar, 'get_target_energy') else 0
        except Exception as e:
            print(f"Warning: Could not get target energy: {e}")
            data['target_energy'] = 0
            
        return data
        
    def detect_motion(self, debug=False):
        """
        Check if motion is detected based on the current sensor readings and thresholds.
        
        Args:
            debug (bool): Whether to print debug information
            
        Returns:
            bool: True if motion is detected, False otherwise
            dict: Dictionary containing the sensor data
        """
        data = self.get_sensor_data()
        
        if data is None:
            return False, None
            
        # Print target data if debug is enabled
        if debug:
            print(f"Target number: {data['target_number']}")
            print(f"Target speed: {data['target_speed']} m/s")
            print(f"Target range: {data['target_range']} cm")
            print(f"Target energy: {data['target_energy']}")

        # Check if motion is detected based on thresholds
        motion_detected = False
        if data['target_number'] > 0:
            motion_detected = self.check_motion_detected(
                data['target_speed'], 
                data['target_range'], 
                data['target_energy'],
                debug
            )
            
        if debug:
            if motion_detected:
                print("\033[91m*** MOTION DETECTED! ***\033[0m")  # Red text for visibility
            else:
                print("No significant motion detected")
            print("-" * 40)
            
        return motion_detected, data
