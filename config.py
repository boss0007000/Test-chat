"""
Configuration settings for the autonomous robot system.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for robot settings."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
    
    # Sensor Configuration
    CAMERA_ENABLED = os.getenv('CAMERA_ENABLED', 'true').lower() == 'true'
    ULTRASONIC_ENABLED = os.getenv('ULTRASONIC_ENABLED', 'true').lower() == 'true'
    LIDAR_ENABLED = os.getenv('LIDAR_ENABLED', 'true').lower() == 'true'
    
    # Camera Settings
    CAMERA_WIDTH = int(os.getenv('CAMERA_WIDTH', '640'))
    CAMERA_HEIGHT = int(os.getenv('CAMERA_HEIGHT', '480'))
    CAMERA_FPS = int(os.getenv('CAMERA_FPS', '30'))
    
    # Ultrasonic Settings
    ULTRASONIC_MAX_DISTANCE = float(os.getenv('ULTRASONIC_MAX_DISTANCE', '400.0'))  # cm
    ULTRASONIC_SENSORS_COUNT = int(os.getenv('ULTRASONIC_SENSORS_COUNT', '4'))
    
    # Lidar Settings
    LIDAR_MAX_RANGE = float(os.getenv('LIDAR_MAX_RANGE', '10.0'))  # meters
    LIDAR_SCAN_RATE = int(os.getenv('LIDAR_SCAN_RATE', '10'))  # Hz
    
    # Robot Settings
    SIMULATION_MODE = os.getenv('SIMULATION_MODE', 'true').lower() == 'true'
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Validate configuration settings."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set. Please set it in .env file.")
        return True
