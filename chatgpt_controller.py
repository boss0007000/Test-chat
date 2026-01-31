"""
ChatGPT integration module for processing sensor data and executing tasks.
"""
import json
from typing import Dict, Any, Optional, List
from openai import OpenAI


class ChatGPTController:
    """Controller for interfacing with ChatGPT API."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initialize ChatGPT controller.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        
        # System prompt for the robot
        self.system_prompt = """You are an AI assistant controlling an autonomous robot equipped with:
1. Camera sensor - Provides visual information about the environment
2. Ultrasonic sensors - Measure distances to nearby objects (in centimeters)
3. Lidar sensor - Provides 360-degree distance scanning (in meters)

Your role is to:
- Analyze sensor data from these inputs
- Understand the robot's environment
- Provide actionable instructions or decisions based on the task given
- Respond with clear, concise, and practical guidance

When analyzing sensor data:
- Consider all available sensor inputs
- Identify obstacles, clear paths, and points of interest
- Provide spatial awareness and navigation suggestions
- Be specific about distances and directions

Always provide your response in a structured format with:
1. Analysis: What you understand from the sensor data
2. Decision: What action or next step should be taken
3. Reasoning: Why this decision is appropriate
"""
        
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
    
    def process_sensor_data(self, sensor_data: Dict[str, Any], user_task: str) -> str:
        """
        Process sensor data with ChatGPT based on user task.
        
        Args:
            sensor_data: Dictionary containing all sensor readings
            user_task: The task/prompt from the user
            
        Returns:
            ChatGPT's response and guidance
        """
        # Format sensor data for ChatGPT
        sensor_summary = self._format_sensor_data(sensor_data)
        
        # Create the user message
        user_message = f"""Task: {user_task}

Current Sensor Data:
{sensor_summary}

Please analyze the sensor data and provide guidance on how to accomplish the task."""
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from ChatGPT
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            error_message = f"Error communicating with ChatGPT: {str(e)}"
            print(error_message)
            return error_message
    
    def process_with_vision(self, sensor_data: Dict[str, Any], user_task: str) -> str:
        """
        Process sensor data with ChatGPT using vision capabilities.
        
        Args:
            sensor_data: Dictionary containing all sensor readings
            user_task: The task/prompt from the user
            
        Returns:
            ChatGPT's response with vision analysis
        """
        # Check if camera data is available
        camera_data = None
        for sensor_name, data in sensor_data.get("sensors", {}).items():
            if data.get("type") == "camera" and data.get("image_base64"):
                camera_data = data
                break
        
        if not camera_data:
            return self.process_sensor_data(sensor_data, user_task)
        
        # Format other sensor data
        sensor_summary = self._format_sensor_data(sensor_data, exclude_camera=True)
        
        # Create message with image
        user_message_text = f"""Task: {user_task}

Current Sensor Data:
{sensor_summary}

Additionally, I'm providing a camera image for visual analysis. Please analyze the image along with other sensor data to provide comprehensive guidance."""
        
        try:
            # Create message with vision
            messages = self.conversation_history.copy()
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": user_message_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{camera_data['image_base64']}"
                        }
                    }
                ]
            })
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add to conversation history (simplified without image)
            self.conversation_history.append({
                "role": "user",
                "content": user_message_text
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            error_message = f"Error with vision processing: {str(e)}"
            print(error_message)
            # Fallback to text-only processing
            return self.process_sensor_data(sensor_data, user_task)
    
    def _format_sensor_data(self, sensor_data: Dict[str, Any], exclude_camera: bool = False) -> str:
        """Format sensor data into readable text for ChatGPT."""
        lines = []
        
        for sensor_name, data in sensor_data.get("sensors", {}).items():
            if data.get("status") == "disabled":
                continue
            
            if data["type"] == "camera" and not exclude_camera:
                lines.append(f"{sensor_name}:")
                lines.append(f"  Status: {data['status']}")
                lines.append(f"  Resolution: {data['width']}x{data['height']}")
                lines.append(f"  {data['description']}")
                
            elif data["type"] == "ultrasonic":
                lines.append(f"{sensor_name}:")
                lines.append(f"  Status: {data['status']}")
                lines.append(f"  Distance: {data['distance_cm']}cm")
                
            elif data["type"] == "lidar":
                lines.append(f"{sensor_name}:")
                lines.append(f"  Status: {data['status']}")
                lines.append(f"  Scan Points: {data['num_points']}")
                lines.append(f"  Max Range: {data['max_range_m']}m")
                
                # Calculate statistics
                scan_data = data["scan_data"]
                distances = [point["distance"] for point in scan_data]
                min_dist = min(distances)
                max_dist = max(distances)
                avg_dist = sum(distances) / len(distances)
                
                lines.append(f"  Nearest obstacle: {min_dist:.2f}m")
                lines.append(f"  Farthest point: {max_dist:.2f}m")
                lines.append(f"  Average distance: {avg_dist:.2f}m")
                
                # Find direction of nearest obstacle
                min_idx = distances.index(min_dist)
                nearest_angle = scan_data[min_idx]["angle"]
                lines.append(f"  Nearest obstacle direction: {nearest_angle:.1f}°")
        
        return "\n".join(lines)
    
    def clear_history(self):
        """Clear conversation history except system prompt."""
        self.conversation_history = [self.conversation_history[0]]
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the full conversation history."""
        return self.conversation_history.copy()
