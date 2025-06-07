from typing import Dict, Any, List
from groq import Groq
import os

class ReasoningAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=api_key)
        self.model = "qwen-qwq-32b"
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 10

    def _update_history(self, user_input: str, response: str):
        self.conversation_history.append({
            "user": user_input,
            "assistant": response
        })
        
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

    def process(self, user_input: str) -> Dict[str, Any]:
        try:
            messages = [
                {"role": "system", "content": "You are an AI assistant with memory and reasoning capabilities. Use the conversation history to provide contextual and well-reasoned responses."}
            ]
            
            for interaction in self.conversation_history:
                messages.extend([
                    {"role": "user", "content": interaction["user"]},
                    {"role": "assistant", "content": interaction["assistant"]}
                ])
            
            messages.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            assistant_response = response.choices[0].message.content
            self._update_history(user_input, assistant_response)
            
            return {
                "success": True,
                "response": assistant_response,
                "agent": "reasoning_agent"
            }
        except Exception as e:
            return {
                "success": False,
                "response": f"Error in ReasoningAgent: {str(e)}",
                "agent": "reasoning_agent"
            } 