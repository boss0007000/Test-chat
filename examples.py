"""
Example script demonstrating how to use the autonomous robot system.
"""
from robot import AutonomousRobot
from config import Config


def example_navigation_task():
    """Example: Navigation task."""
    print("Example 1: Navigation Task")
    print("-" * 60)
    
    robot = AutonomousRobot()
    task = "Navigate forward while avoiding obstacles. Suggest the best direction to move."
    response = robot.run_single_task(task)
    
    print(f"\nTask: {task}")
    print(f"\nResponse:\n{response}")
    print("-" * 60)


def example_object_detection():
    """Example: Object detection task."""
    print("\nExample 2: Object Detection Task")
    print("-" * 60)
    
    robot = AutonomousRobot()
    task = "Analyze the camera feed and identify any objects or obstacles in view."
    response = robot.run_single_task(task)
    
    print(f"\nTask: {task}")
    print(f"\nResponse:\n{response}")
    print("-" * 60)


def example_environment_mapping():
    """Example: Environment mapping task."""
    print("\nExample 3: Environment Mapping Task")
    print("-" * 60)
    
    robot = AutonomousRobot()
    task = "Create a description of the surrounding environment based on all sensor data."
    response = robot.run_single_task(task)
    
    print(f"\nTask: {task}")
    print(f"\nResponse:\n{response}")
    print("-" * 60)


def example_safety_check():
    """Example: Safety check task."""
    print("\nExample 4: Safety Check Task")
    print("-" * 60)
    
    robot = AutonomousRobot()
    task = "Perform a safety check. Are there any obstacles too close? Is it safe to move?"
    response = robot.run_single_task(task)
    
    print(f"\nTask: {task}")
    print(f"\nResponse:\n{response}")
    print("-" * 60)


def example_custom_task():
    """Example: Custom task with user input."""
    print("\nExample 5: Custom Task")
    print("-" * 60)
    
    robot = AutonomousRobot()
    
    # Get custom task from user
    task = input("Enter your custom task: ")
    response = robot.run_single_task(task)
    
    print(f"\nTask: {task}")
    print(f"\nResponse:\n{response}")
    print("-" * 60)


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("AUTONOMOUS ROBOT - EXAMPLE DEMONSTRATIONS")
    print("="*60)
    
    try:
        # Run examples
        example_navigation_task()
        example_object_detection()
        example_environment_mapping()
        example_safety_check()
        
        # Ask if user wants to try custom task
        print("\nWould you like to try a custom task? (yes/no)")
        choice = input("> ").strip().lower()
        if choice in ['yes', 'y']:
            example_custom_task()
        
        print("\n" + "="*60)
        print("Examples completed!")
        print("="*60)
        
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file in the project directory")
        print("2. Added your OpenAI API key: OPENAI_API_KEY=your_key_here")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
