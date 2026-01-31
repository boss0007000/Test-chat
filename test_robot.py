"""
Unit tests for the autonomous robot system.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from config import Config
from sensors import CameraSensor, UltrasonicSensor, LidarSensor, SensorArray
from chatgpt_controller import ChatGPTController


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    def test_config_defaults(self):
        """Test default configuration values."""
        config = Config()
        self.assertEqual(config.OPENAI_MODEL, 'gpt-4o')
        self.assertTrue(config.SIMULATION_MODE)
        self.assertTrue(config.CAMERA_ENABLED)
    
    def test_config_validation_fails_without_api_key(self):
        """Test config validation fails without API key."""
        config = Config()
        config.OPENAI_API_KEY = ''
        with self.assertRaises(ValueError):
            config.validate()


class TestSensors(unittest.TestCase):
    """Test sensor implementations."""
    
    def test_camera_sensor_initialization(self):
        """Test camera sensor can be initialized."""
        camera = CameraSensor(simulation_mode=True)
        self.assertEqual(camera.name, "Camera")
        self.assertTrue(camera.simulation_mode)
        self.assertTrue(camera.enabled)
    
    def test_camera_sensor_read_simulated(self):
        """Test camera sensor reading in simulation mode."""
        camera = CameraSensor(width=640, height=480, simulation_mode=True)
        data = camera.read()
        
        self.assertEqual(data['type'], 'camera')
        self.assertEqual(data['status'], 'simulated')
        self.assertEqual(data['width'], 640)
        self.assertEqual(data['height'], 480)
        self.assertIn('image_base64', data)
        self.assertIn('timestamp', data)
    
    def test_ultrasonic_sensor_initialization(self):
        """Test ultrasonic sensor initialization."""
        sensor = UltrasonicSensor(sensor_id=0, simulation_mode=True)
        self.assertEqual(sensor.name, "Ultrasonic_0")
        self.assertEqual(sensor.sensor_id, 0)
        self.assertTrue(sensor.enabled)
    
    def test_ultrasonic_sensor_read_simulated(self):
        """Test ultrasonic sensor reading."""
        sensor = UltrasonicSensor(sensor_id=0, max_distance=400.0, simulation_mode=True)
        data = sensor.read()
        
        self.assertEqual(data['type'], 'ultrasonic')
        self.assertEqual(data['sensor_id'], 0)
        self.assertEqual(data['status'], 'simulated')
        self.assertIn('distance_cm', data)
        self.assertGreater(data['distance_cm'], 0)
        self.assertLessEqual(data['distance_cm'], 400.0)
    
    def test_lidar_sensor_initialization(self):
        """Test lidar sensor initialization."""
        lidar = LidarSensor(max_range=10.0, simulation_mode=True)
        self.assertEqual(lidar.name, "Lidar")
        self.assertEqual(lidar.max_range, 10.0)
        self.assertTrue(lidar.enabled)
    
    def test_lidar_sensor_read_simulated(self):
        """Test lidar sensor reading."""
        lidar = LidarSensor(max_range=10.0, num_points=360, simulation_mode=True)
        data = lidar.read()
        
        self.assertEqual(data['type'], 'lidar')
        self.assertEqual(data['status'], 'simulated')
        self.assertEqual(data['num_points'], 360)
        self.assertIn('scan_data', data)
        self.assertEqual(len(data['scan_data']), 360)
        
        # Check scan data structure
        point = data['scan_data'][0]
        self.assertIn('angle', point)
        self.assertIn('distance', point)
    
    def test_sensor_enable_disable(self):
        """Test sensor enable/disable functionality."""
        sensor = UltrasonicSensor(sensor_id=0, simulation_mode=True)
        
        # Test disable
        sensor.disable()
        self.assertFalse(sensor.enabled)
        data = sensor.read()
        self.assertEqual(data['status'], 'disabled')
        
        # Test enable
        sensor.enable()
        self.assertTrue(sensor.enabled)
        data = sensor.read()
        self.assertNotEqual(data['status'], 'disabled')


class TestSensorArray(unittest.TestCase):
    """Test sensor array functionality."""
    
    def setUp(self):
        """Set up test configuration."""
        self.config = Config()
        self.config.SIMULATION_MODE = True
        self.config.CAMERA_ENABLED = True
        self.config.ULTRASONIC_ENABLED = True
        self.config.LIDAR_ENABLED = True
        self.config.ULTRASONIC_SENSORS_COUNT = 4
    
    def test_sensor_array_initialization(self):
        """Test sensor array initialization."""
        array = SensorArray(self.config)
        
        self.assertIsNotNone(array.camera)
        self.assertEqual(len(array.ultrasonic_sensors), 4)
        self.assertIsNotNone(array.lidar)
        self.assertEqual(len(array.sensors), 6)  # 1 camera + 4 ultrasonic + 1 lidar
    
    def test_sensor_array_read_all(self):
        """Test reading all sensors."""
        array = SensorArray(self.config)
        data = array.read_all()
        
        self.assertIn('timestamp', data)
        self.assertIn('sensors', data)
        self.assertIn('Camera', data['sensors'])
        self.assertIn('Lidar', data['sensors'])
        self.assertIn('Ultrasonic_0', data['sensors'])
    
    def test_sensor_array_summary(self):
        """Test sensor summary generation."""
        array = SensorArray(self.config)
        summary = array.get_sensor_summary()
        
        self.assertIsInstance(summary, str)
        self.assertIn('Camera', summary)
        self.assertIn('Lidar', summary)
        self.assertIn('Ultrasonic', summary)


class TestChatGPTController(unittest.TestCase):
    """Test ChatGPT controller."""
    
    def setUp(self):
        """Set up mock OpenAI client."""
        self.api_key = "test_api_key"
        self.model = "gpt-4o"
    
    @patch('chatgpt_controller.OpenAI')
    def test_chatgpt_controller_initialization(self, mock_openai):
        """Test ChatGPT controller initialization."""
        controller = ChatGPTController(self.api_key, self.model)
        
        self.assertEqual(controller.model, self.model)
        self.assertIsNotNone(controller.system_prompt)
        self.assertEqual(len(controller.conversation_history), 1)
        self.assertEqual(controller.conversation_history[0]['role'], 'system')
    
    @patch('chatgpt_controller.OpenAI')
    def test_format_sensor_data(self, mock_openai):
        """Test sensor data formatting."""
        controller = ChatGPTController(self.api_key, self.model)
        
        sensor_data = {
            "sensors": {
                "Camera": {
                    "type": "camera",
                    "status": "simulated",
                    "width": 640,
                    "height": 480,
                    "description": "Test image"
                },
                "Ultrasonic_0": {
                    "type": "ultrasonic",
                    "status": "simulated",
                    "sensor_id": 0,
                    "distance_cm": 50.0
                }
            }
        }
        
        formatted = controller._format_sensor_data(sensor_data)
        self.assertIsInstance(formatted, str)
        self.assertIn('Camera', formatted)
        self.assertIn('Ultrasonic', formatted)
    
    @patch('chatgpt_controller.OpenAI')
    def test_clear_history(self, mock_openai):
        """Test conversation history clearing."""
        controller = ChatGPTController(self.api_key, self.model)
        
        # Add some messages
        controller.conversation_history.append({"role": "user", "content": "test"})
        controller.conversation_history.append({"role": "assistant", "content": "response"})
        
        self.assertEqual(len(controller.conversation_history), 3)
        
        # Clear history
        controller.clear_history()
        
        self.assertEqual(len(controller.conversation_history), 1)
        self.assertEqual(controller.conversation_history[0]['role'], 'system')


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    @patch('chatgpt_controller.OpenAI')
    def test_full_system_integration(self, mock_openai):
        """Test full system integration."""
        # Mock OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response from ChatGPT"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Create configuration
        config = Config()
        config.OPENAI_API_KEY = "test_key"
        config.SIMULATION_MODE = True
        
        # Create sensor array
        sensors = SensorArray(config)
        
        # Create ChatGPT controller
        chatgpt = ChatGPTController(config.OPENAI_API_KEY, config.OPENAI_MODEL)
        
        # Collect sensor data
        sensor_data = sensors.read_all()
        
        # Process with ChatGPT
        response = chatgpt.process_sensor_data(sensor_data, "Test task")
        
        self.assertEqual(response, "Test response from ChatGPT")
        self.assertTrue(mock_client.chat.completions.create.called)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
