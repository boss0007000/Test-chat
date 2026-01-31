# Autonomous Robot with ChatGPT Integration

An intelligent autonomous robot system that integrates camera, ultrasonic sensors, and lidar with ChatGPT to perform tasks based on natural language prompts.

## Features

- **Multi-Sensor Integration**
  - 📷 Camera sensor for visual data capture
  - 📡 Ultrasonic sensors for distance measurement
  - 🔄 Lidar sensor for 360-degree environmental scanning

- **ChatGPT Integration**
  - Natural language task input
  - AI-powered decision making
  - Vision-enabled analysis (GPT-4o)
  - Context-aware responses

- **Flexible Operation Modes**
  - Simulation mode for testing without hardware
  - Real hardware mode for physical robots
  - Interactive and programmatic interfaces

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/boss0007000/Test-chat.git
cd Test-chat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Interactive Mode

Run the robot in interactive mode to input tasks via command line:

```bash
python robot.py
```

This will:
1. Initialize all sensors
2. Prompt you to enter a task
3. Collect sensor data
4. Process with ChatGPT
5. Display AI-generated guidance

### Programmatic Usage

Use the robot in your own Python code:

```python
from robot import AutonomousRobot

# Create robot instance
robot = AutonomousRobot()

# Execute a task
task = "Navigate forward while avoiding obstacles"
response = robot.run_single_task(task)
print(response)
```

### Example Demonstrations

Run the provided examples to see various use cases:

```bash
python examples.py
```

This demonstrates:
- Navigation tasks
- Object detection
- Environment mapping
- Safety checks
- Custom tasks

## Architecture

### Components

1. **config.py** - Configuration management with environment variables
2. **sensors.py** - Sensor interfaces (Camera, Ultrasonic, Lidar)
3. **chatgpt_controller.py** - OpenAI API integration
4. **robot.py** - Main robot controller
5. **examples.py** - Example use cases

### Sensor Data Flow

```
Sensors → Data Collection → ChatGPT Processing → Task Execution
   ↓            ↓                    ↓                  ↓
Camera    Image Capture        Vision Analysis    Guidance
Ultrasonic   Distance          Obstacle Detection Navigation
Lidar     360° Scan           Spatial Awareness  Path Planning
```

## Configuration

All settings can be configured via environment variables in `.env`:

### OpenAI Settings
- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - Model to use (default: gpt-4o)

### Sensor Settings
- `CAMERA_ENABLED` - Enable/disable camera (default: true)
- `ULTRASONIC_ENABLED` - Enable/disable ultrasonic sensors (default: true)
- `LIDAR_ENABLED` - Enable/disable lidar (default: true)

### Camera Settings
- `CAMERA_WIDTH` - Camera resolution width (default: 640)
- `CAMERA_HEIGHT` - Camera resolution height (default: 480)
- `CAMERA_FPS` - Camera frame rate (default: 30)

### Ultrasonic Settings
- `ULTRASONIC_MAX_DISTANCE` - Max detection distance in cm (default: 400.0)
- `ULTRASONIC_SENSORS_COUNT` - Number of sensors (default: 4)

### Lidar Settings
- `LIDAR_MAX_RANGE` - Max range in meters (default: 10.0)
- `LIDAR_SCAN_RATE` - Scan rate in Hz (default: 10)

### Robot Settings
- `SIMULATION_MODE` - Use simulated sensors (default: true)
- `DEBUG_MODE` - Enable debug output (default: false)

## Example Tasks

Here are some example tasks you can give the robot:

1. **Navigation**: "Navigate forward while avoiding obstacles"
2. **Object Detection**: "Identify objects in the camera view"
3. **Mapping**: "Describe the environment around the robot"
4. **Safety**: "Check if it's safe to move forward"
5. **Path Planning**: "Find the best path to move through the space"
6. **Obstacle Avoidance**: "Which direction has the most clearance?"

## Hardware Integration

### For Real Hardware

To use with real sensors, set `SIMULATION_MODE=false` in your `.env` file and ensure:

1. **Camera**: Compatible webcam or camera module
2. **Ultrasonic**: HC-SR04 or similar sensors with GPIO interface
3. **Lidar**: Compatible lidar scanner with appropriate drivers

Modify the sensor classes in `sensors.py` to add your specific hardware interfaces.

## Development

### Project Structure

```
Test-chat/
├── robot.py                 # Main robot controller
├── sensors.py              # Sensor implementations
├── chatgpt_controller.py   # ChatGPT integration
├── config.py               # Configuration management
├── examples.py             # Example demonstrations
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

### Adding Custom Sensors

Extend the `BaseSensor` class in `sensors.py`:

```python
class CustomSensor(BaseSensor):
    def __init__(self, simulation_mode=True):
        super().__init__("CustomSensor", simulation_mode)
    
    def read(self):
        # Implement sensor reading logic
        return {"type": "custom", "data": ...}
```

### Extending Functionality

Add custom processing in `chatgpt_controller.py` or create new methods in `AutonomousRobot` class.

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `OPENAI_API_KEY` is set correctly in `.env`
2. **Camera Not Found**: Set `SIMULATION_MODE=true` for testing without hardware
3. **Import Errors**: Run `pip install -r requirements.txt`

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.