"""
Sensor interface modules for camera, ultrasonic, and lidar sensors.
"""
import time
import base64
from io import BytesIO
from typing import Dict, Any, List, Optional
import numpy as np

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from PIL import Image
except ImportError:
    Image = None


class BaseSensor:
    """Base class for all sensors."""
    
    def __init__(self, name: str, simulation_mode: bool = True):
        self.name = name
        self.simulation_mode = simulation_mode
        self.enabled = True
    
    def read(self) -> Dict[str, Any]:
        """Read data from the sensor."""
        raise NotImplementedError("Subclasses must implement read method")
    
    def enable(self):
        """Enable the sensor."""
        self.enabled = True
    
    def disable(self):
        """Disable the sensor."""
        self.enabled = False


class CameraSensor(BaseSensor):
    """Camera sensor for visual data capture."""
    
    def __init__(self, width: int = 640, height: int = 480, simulation_mode: bool = True):
        super().__init__("Camera", simulation_mode)
        self.width = width
        self.height = height
        self.capture = None
        
        if not simulation_mode and cv2 is not None:
            try:
                self.capture = cv2.VideoCapture(0)
                self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            except Exception as e:
                print(f"Warning: Could not initialize camera: {e}. Using simulation mode.")
                self.simulation_mode = True
    
    def read(self) -> Dict[str, Any]:
        """Capture image from camera."""
        if not self.enabled:
            return {"type": "camera", "status": "disabled", "data": None}
        
        if self.simulation_mode or self.capture is None:
            # Simulated camera data
            image = np.random.randint(0, 255, (self.height, self.width, 3), dtype=np.uint8)
            image_base64 = self._encode_image(image)
            
            return {
                "type": "camera",
                "status": "simulated",
                "width": self.width,
                "height": self.height,
                "timestamp": time.time(),
                "image_base64": image_base64,
                "description": "Simulated camera image with random noise pattern"
            }
        else:
            # Real camera data
            ret, frame = self.capture.read()
            if ret:
                image_base64 = self._encode_image(frame)
                return {
                    "type": "camera",
                    "status": "active",
                    "width": frame.shape[1],
                    "height": frame.shape[0],
                    "timestamp": time.time(),
                    "image_base64": image_base64,
                    "description": "Real camera image captured from device"
                }
            else:
                return {
                    "type": "camera",
                    "status": "error",
                    "error": "Failed to capture frame"
                }
    
    def _encode_image(self, image: np.ndarray) -> str:
        """Encode image to base64 string."""
        if cv2 is not None:
            _, buffer = cv2.imencode('.jpg', image)
            return base64.b64encode(buffer).decode('utf-8')
        elif Image is not None:
            pil_image = Image.fromarray(image)
            buffer = BytesIO()
            pil_image.save(buffer, format='JPEG')
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
        else:
            return ""
    
    def __del__(self):
        """Release camera resources."""
        if self.capture is not None:
            self.capture.release()


class UltrasonicSensor(BaseSensor):
    """Ultrasonic distance sensor."""
    
    def __init__(self, sensor_id: int, max_distance: float = 400.0, simulation_mode: bool = True):
        super().__init__(f"Ultrasonic_{sensor_id}", simulation_mode)
        self.sensor_id = sensor_id
        self.max_distance = max_distance  # Maximum distance in cm
    
    def read(self) -> Dict[str, Any]:
        """Read distance measurement from ultrasonic sensor."""
        if not self.enabled:
            return {"type": "ultrasonic", "sensor_id": self.sensor_id, "status": "disabled", "data": None}
        
        if self.simulation_mode:
            # Simulated ultrasonic data - random distance with some variance
            distance = np.random.uniform(5.0, self.max_distance)
            
            return {
                "type": "ultrasonic",
                "sensor_id": self.sensor_id,
                "status": "simulated",
                "distance_cm": round(distance, 2),
                "max_distance_cm": self.max_distance,
                "timestamp": time.time(),
                "description": f"Simulated distance measurement: {round(distance, 2)}cm"
            }
        else:
            # Real sensor reading would go here
            # For now, return simulated data
            distance = np.random.uniform(5.0, self.max_distance)
            return {
                "type": "ultrasonic",
                "sensor_id": self.sensor_id,
                "status": "active",
                "distance_cm": round(distance, 2),
                "max_distance_cm": self.max_distance,
                "timestamp": time.time(),
                "description": f"Distance measurement: {round(distance, 2)}cm"
            }


class LidarSensor(BaseSensor):
    """Lidar sensor for 360-degree distance scanning."""
    
    def __init__(self, max_range: float = 10.0, num_points: int = 360, simulation_mode: bool = True):
        super().__init__("Lidar", simulation_mode)
        self.max_range = max_range  # Maximum range in meters
        self.num_points = num_points  # Number of scan points
    
    def read(self) -> Dict[str, Any]:
        """Read lidar scan data."""
        if not self.enabled:
            return {"type": "lidar", "status": "disabled", "data": None}
        
        if self.simulation_mode:
            # Simulated lidar data - generate random point cloud
            angles = np.linspace(0, 360, self.num_points, endpoint=False)
            distances = np.random.uniform(0.1, self.max_range, self.num_points)
            
            # Create some obstacles for realism
            for i in range(3):
                obstacle_angle = np.random.uniform(0, 360)
                obstacle_width = np.random.uniform(10, 30)
                obstacle_distance = np.random.uniform(0.5, self.max_range * 0.7)
                
                mask = np.abs(angles - obstacle_angle) < obstacle_width
                distances[mask] = obstacle_distance
            
            scan_data = [
                {"angle": float(angle), "distance": float(dist)}
                for angle, dist in zip(angles, distances)
            ]
            
            return {
                "type": "lidar",
                "status": "simulated",
                "max_range_m": self.max_range,
                "num_points": self.num_points,
                "timestamp": time.time(),
                "scan_data": scan_data,
                "description": f"Simulated 360-degree lidar scan with {self.num_points} points"
            }
        else:
            # Real lidar reading would go here
            angles = np.linspace(0, 360, self.num_points, endpoint=False)
            distances = np.random.uniform(0.1, self.max_range, self.num_points)
            
            scan_data = [
                {"angle": float(angle), "distance": float(dist)}
                for angle, dist in zip(angles, distances)
            ]
            
            return {
                "type": "lidar",
                "status": "active",
                "max_range_m": self.max_range,
                "num_points": self.num_points,
                "timestamp": time.time(),
                "scan_data": scan_data,
                "description": f"360-degree lidar scan with {self.num_points} points"
            }


class SensorArray:
    """Collection of all sensors for the robot."""
    
    def __init__(self, config):
        self.sensors: List[BaseSensor] = []
        
        # Initialize camera
        if config.CAMERA_ENABLED:
            self.camera = CameraSensor(
                width=config.CAMERA_WIDTH,
                height=config.CAMERA_HEIGHT,
                simulation_mode=config.SIMULATION_MODE
            )
            self.sensors.append(self.camera)
        else:
            self.camera = None
        
        # Initialize ultrasonic sensors
        self.ultrasonic_sensors = []
        if config.ULTRASONIC_ENABLED:
            for i in range(config.ULTRASONIC_SENSORS_COUNT):
                sensor = UltrasonicSensor(
                    sensor_id=i,
                    max_distance=config.ULTRASONIC_MAX_DISTANCE,
                    simulation_mode=config.SIMULATION_MODE
                )
                self.ultrasonic_sensors.append(sensor)
                self.sensors.append(sensor)
        
        # Initialize lidar
        if config.LIDAR_ENABLED:
            self.lidar = LidarSensor(
                max_range=config.LIDAR_MAX_RANGE,
                simulation_mode=config.SIMULATION_MODE
            )
            self.sensors.append(self.lidar)
        else:
            self.lidar = None
    
    def read_all(self) -> Dict[str, Any]:
        """Read data from all enabled sensors."""
        data = {
            "timestamp": time.time(),
            "sensors": {}
        }
        
        for sensor in self.sensors:
            if sensor.enabled:
                sensor_data = sensor.read()
                data["sensors"][sensor.name] = sensor_data
        
        return data
    
    def get_sensor_summary(self) -> str:
        """Get a text summary of sensor readings for ChatGPT."""
        data = self.read_all()
        summary_parts = []
        
        summary_parts.append(f"Sensor Data Summary (Timestamp: {data['timestamp']:.2f})")
        summary_parts.append("-" * 60)
        
        for sensor_name, sensor_data in data["sensors"].items():
            if sensor_data.get("status") == "disabled":
                continue
                
            if sensor_data["type"] == "camera":
                summary_parts.append(f"\n{sensor_name}:")
                summary_parts.append(f"  Status: {sensor_data['status']}")
                summary_parts.append(f"  Resolution: {sensor_data['width']}x{sensor_data['height']}")
                summary_parts.append(f"  Description: {sensor_data['description']}")
                
            elif sensor_data["type"] == "ultrasonic":
                summary_parts.append(f"\n{sensor_name}:")
                summary_parts.append(f"  Status: {sensor_data['status']}")
                summary_parts.append(f"  Distance: {sensor_data['distance_cm']}cm")
                
            elif sensor_data["type"] == "lidar":
                summary_parts.append(f"\n{sensor_name}:")
                summary_parts.append(f"  Status: {sensor_data['status']}")
                summary_parts.append(f"  Points: {sensor_data['num_points']}")
                summary_parts.append(f"  Max Range: {sensor_data['max_range_m']}m")
                
                # Calculate basic statistics
                scan_data = sensor_data["scan_data"]
                distances = [point["distance"] for point in scan_data]
                min_dist = min(distances)
                avg_dist = sum(distances) / len(distances)
                
                summary_parts.append(f"  Nearest obstacle: {min_dist:.2f}m")
                summary_parts.append(f"  Average distance: {avg_dist:.2f}m")
        
        return "\n".join(summary_parts)
