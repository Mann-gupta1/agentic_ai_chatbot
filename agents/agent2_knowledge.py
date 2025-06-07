from typing import Dict, Any
from groq import Groq
import os

class KnowledgeAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=api_key)
        self.model = "qwen-qwq-32b"
        self.knowledge_base = {}

    def _get_relevant_context(self, query: str) -> str:
        return "Context: Relevant information from the knowledge base."

    def process(self, user_input: str) -> Dict[str, Any]:
        try:
            context = self._get_relevant_context(user_input)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a knowledgeable AI assistant with access to a vast knowledge base."},
                    {"role": "system", "content": f"Context: {context}"},
                    {"role": "user", "content": user_input}
                ]
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "agent": "knowledge_agent"
            }
        except Exception as e:
            return {
                "success": False,
                "response": f"Error in KnowledgeAgent: {str(e)}",
                "agent": "knowledge_agent"
            } 