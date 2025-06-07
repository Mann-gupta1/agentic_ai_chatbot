from typing import Dict, Any
from groq import Groq
import os

class DirectAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=api_key)
        self.model = "qwen-qwq-32b"

    def process(self, user_input: str) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant focused on direct and concise responses."},
                    {"role": "user", "content": user_input}
                ]
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "agent": "direct_agent"
            }
        except Exception as e:
            return {
                "success": False,
                "response": f"Error in DirectAgent: {str(e)}",
                "agent": "direct_agent"
            } 