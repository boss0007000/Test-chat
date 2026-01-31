# Quick Reference Guide

## Quick Start (1 minute)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here

# 3. Test the system
python quickstart.py

# 4. Run the robot
python robot.py
```

## Common Commands

```bash
# Run interactive robot
python robot.py

# Run examples
python examples.py

# Run tests
python -m unittest test_robot.py

# Quick verification
python quickstart.py
```

## Using the Robot

### Interactive Mode
```bash
python robot.py
# Enter tasks when prompted, e.g.:
# > Navigate forward avoiding obstacles
# > Describe what you see in the camera
# > Find the nearest obstacle
```

### Programmatic Mode
```python
from robot import AutonomousRobot

# Create robot
robot = AutonomousRobot()

# Execute task
response = robot.run_single_task("Your task here")
print(response)
```

## Configuration Quick Reference

### Minimal Setup (.env)
```bash
OPENAI_API_KEY=your_key_here
```

### Full Configuration (.env)
```bash
# API
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o

# Mode
SIMULATION_MODE=true
DEBUG_MODE=false

# Sensors
CAMERA_ENABLED=true
ULTRASONIC_ENABLED=true
LIDAR_ENABLED=true

# Camera
CAMERA_WIDTH=640
CAMERA_HEIGHT=480

# Ultrasonic
ULTRASONIC_SENSORS_COUNT=4
ULTRASONIC_MAX_DISTANCE=400.0

# Lidar
LIDAR_MAX_RANGE=10.0
```

## Example Tasks

**Navigation**
```
Navigate forward while avoiding obstacles
Find the safest direction to move
Which way has the most clearance?
```

**Perception**
```
Describe what you see in the camera
Identify objects in the environment
What obstacles are nearby?
```

**Safety**
```
Is it safe to move forward?
Check for obstacles in all directions
Perform a safety assessment
```

**Mapping**
```
Create a map of the surroundings
Describe the environment layout
Where are the obstacles located?
```

## Troubleshooting

### API Key Error
```bash
# Error: OPENAI_API_KEY is not set
# Solution: Add key to .env file
echo "OPENAI_API_KEY=your_key" >> .env
```

### Import Errors
```bash
# Error: No module named 'openai'
# Solution: Install dependencies
pip install -r requirements.txt
```

### Camera Not Found
```bash
# Error: Could not initialize camera
# Solution: Use simulation mode
# In .env: SIMULATION_MODE=true
```

## File Overview

| File | Purpose | Lines |
|------|---------|-------|
| `robot.py` | Main robot controller | 181 |
| `sensors.py` | Sensor implementations | 313 |
| `chatgpt_controller.py` | ChatGPT integration | 229 |
| `config.py` | Configuration | 44 |
| `examples.py` | Usage examples | 117 |
| `test_robot.py` | Unit tests | 259 |
| `quickstart.py` | Quick verification | 78 |

## API Reference

### AutonomousRobot Class
```python
from robot import AutonomousRobot

# Initialize
robot = AutonomousRobot(config=None)

# Run interactive mode
robot.run_interactive()

# Execute single task
response = robot.run_single_task(task: str) -> str

# Execute with options
response = robot.execute_task(task: str, use_vision: bool = True)

# Shutdown
robot.shutdown()
```

### SensorArray Class
```python
from sensors import SensorArray
from config import Config

# Initialize
config = Config()
sensors = SensorArray(config)

# Read all sensors
data = sensors.read_all()

# Get summary
summary = sensors.get_sensor_summary()
```

### ChatGPTController Class
```python
from chatgpt_controller import ChatGPTController

# Initialize
chatgpt = ChatGPTController(api_key: str, model: str = "gpt-4o")

# Process sensor data
response = chatgpt.process_sensor_data(sensor_data: dict, task: str)

# Process with vision
response = chatgpt.process_with_vision(sensor_data: dict, task: str)

# Clear history
chatgpt.clear_history()
```

## Testing

```bash
# Run all tests
python -m unittest test_robot.py -v

# Run specific test
python -m unittest test_robot.TestSensors.test_camera_sensor_read_simulated

# Quick test
python quickstart.py
```

## Development

### Adding a New Sensor
```python
from sensors import BaseSensor

class MySensor(BaseSensor):
    def __init__(self, simulation_mode=True):
        super().__init__("MySensor", simulation_mode)
    
    def read(self):
        return {
            "type": "my_sensor",
            "status": "active",
            "data": your_data
        }
```

### Custom Task Processing
```python
from robot import AutonomousRobot

class MyRobot(AutonomousRobot):
    def custom_task(self, task):
        # Your custom logic
        return self.execute_task(task)
```

## Support

- **Documentation**: README.md, ARCHITECTURE.md
- **Examples**: examples.py
- **Tests**: test_robot.py
- **Issues**: GitHub Issues

## License

MIT License - Open Source
