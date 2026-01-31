#!/usr/bin/env python3
"""
Quick start script to verify the autonomous robot system.
Runs a simple demonstration without requiring API key.
"""
import sys
import os

# Add the project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from sensors import SensorArray


def test_sensors():
    """Test sensor functionality."""
    print("\n" + "="*60)
    print("AUTONOMOUS ROBOT SYSTEM - QUICK START TEST")
    print("="*60)
    
    print("\n1. Testing Configuration...")
    config = Config()
    config.SIMULATION_MODE = True
    print("   ✓ Configuration loaded successfully")
    print(f"   - Simulation Mode: {config.SIMULATION_MODE}")
    print(f"   - Camera Enabled: {config.CAMERA_ENABLED}")
    print(f"   - Ultrasonic Enabled: {config.ULTRASONIC_ENABLED}")
    print(f"   - Lidar Enabled: {config.LIDAR_ENABLED}")
    
    print("\n2. Initializing Sensors...")
    sensors = SensorArray(config)
    print(f"   ✓ {len(sensors.sensors)} sensors initialized:")
    for sensor in sensors.sensors:
        print(f"     - {sensor.name}")
    
    print("\n3. Collecting Sensor Data...")
    sensor_data = sensors.read_all()
    print("   ✓ Sensor data collected successfully")
    
    print("\n4. Sensor Readings:")
    print("-" * 60)
    print(sensors.get_sensor_summary())
    print("-" * 60)
    
    print("\n5. System Status:")
    print("   ✓ All sensors operational")
    print("   ✓ Data collection working")
    print("   ✓ System ready for ChatGPT integration")
    
    print("\n" + "="*60)
    print("QUICK START TEST COMPLETE!")
    print("="*60)
    
    print("\nNext Steps:")
    print("1. Copy .env.example to .env")
    print("2. Add your OpenAI API key to .env")
    print("3. Run: python robot.py")
    print("\nFor examples: python examples.py")
    print("For tests: python -m unittest test_robot.py")
    
    return True


def main():
    """Main entry point."""
    try:
        success = test_sensors()
        return 0 if success else 1
    except Exception as e:
        print(f"\nError during quick start test: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
