"""
Main autonomous robot controller integrating sensors and ChatGPT.
"""
import time
from typing import Optional
from config import Config
from sensors import SensorArray
from chatgpt_controller import ChatGPTController


class AutonomousRobot:
    """Main controller for the autonomous robot system."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the autonomous robot.
        
        Args:
            config: Configuration object (uses default Config if None)
        """
        self.config = config or Config()
        
        # Validate configuration
        self.config.validate()
        
        # Initialize sensor array
        print("Initializing sensors...")
        self.sensors = SensorArray(self.config)
        
        # Initialize ChatGPT controller
        print("Initializing ChatGPT controller...")
        self.chatgpt = ChatGPTController(
            api_key=self.config.OPENAI_API_KEY,
            model=self.config.OPENAI_MODEL
        )
        
        self.running = False
        print("Robot initialization complete!")
    
    def get_task_from_user(self) -> str:
        """
        Get task/prompt from the user.
        
        Returns:
            User's task description
        """
        print("\n" + "="*60)
        print("AUTONOMOUS ROBOT - TASK INPUT")
        print("="*60)
        task = input("\nPlease enter the task you want the robot to perform:\n> ")
        return task.strip()
    
    def execute_task(self, task: str, use_vision: bool = True) -> str:
        """
        Execute a task using sensor data and ChatGPT.
        
        Args:
            task: The task description from user
            use_vision: Whether to use vision capabilities (default: True)
            
        Returns:
            ChatGPT's response/guidance
        """
        print(f"\nExecuting task: {task}")
        print("-" * 60)
        
        # Collect sensor data
        print("Collecting sensor data...")
        sensor_data = self.sensors.read_all()
        
        # Display sensor summary
        if self.config.DEBUG_MODE:
            print("\nSensor Summary:")
            print(self.sensors.get_sensor_summary())
            print("-" * 60)
        
        # Process with ChatGPT
        print("Processing with ChatGPT...")
        if use_vision and self.sensors.camera is not None:
            response = self.chatgpt.process_with_vision(sensor_data, task)
        else:
            response = self.chatgpt.process_sensor_data(sensor_data, task)
        
        return response
    
    def run_interactive(self):
        """Run the robot in interactive mode."""
        print("\n" + "="*60)
        print("AUTONOMOUS ROBOT SYSTEM")
        print("="*60)
        print(f"Mode: {'SIMULATION' if self.config.SIMULATION_MODE else 'REAL HARDWARE'}")
        print(f"Model: {self.config.OPENAI_MODEL}")
        print("\nActive Sensors:")
        for sensor in self.sensors.sensors:
            print(f"  - {sensor.name}")
        print("="*60)
        
        self.running = True
        
        while self.running:
            try:
                # Get task from user
                task = self.get_task_from_user()
                
                if not task:
                    print("No task entered. Please try again.")
                    continue
                
                # Check for exit commands
                if task.lower() in ['exit', 'quit', 'q']:
                    print("Shutting down robot...")
                    self.running = False
                    break
                
                # Execute the task
                response = self.execute_task(task)
                
                # Display response
                print("\n" + "="*60)
                print("CHATGPT RESPONSE:")
                print("="*60)
                print(response)
                print("="*60)
                
                # Ask if user wants to continue
                print("\nPress Enter to continue with another task, or type 'exit' to quit...")
                continue_input = input("> ").strip().lower()
                if continue_input in ['exit', 'quit', 'q']:
                    print("Shutting down robot...")
                    self.running = False
                    break
                
            except KeyboardInterrupt:
                print("\n\nShutting down robot...")
                self.running = False
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again or type 'exit' to quit.")
    
    def run_single_task(self, task: str) -> str:
        """
        Run a single task and return the response.
        
        Args:
            task: Task description
            
        Returns:
            ChatGPT's response
        """
        return self.execute_task(task)
    
    def shutdown(self):
        """Shutdown the robot and cleanup resources."""
        print("Cleaning up resources...")
        self.running = False
        # Sensor cleanup is handled by their destructors


def main():
    """Main entry point for the robot system."""
    try:
        # Create and run robot
        robot = AutonomousRobot()
        robot.run_interactive()
        
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file in the project directory")
        print("2. Added your OpenAI API key: OPENAI_API_KEY=your_key_here")
        return 1
    except Exception as e:
        print(f"\nUnexpected Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
