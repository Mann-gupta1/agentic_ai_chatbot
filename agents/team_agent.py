from typing import Dict, Any
from groq import Groq
import os
from agents.agent1_direct import DirectAgent
from agents.agent2_knowledge import KnowledgeAgent
from agents.agent3_reasoning import ReasoningAgent
from agents.agent4_memory import MemoryAgent
from agents.agent5_rag import RAGAgent

class TeamAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        self.client = Groq(api_key=api_key)
        self.model = "qwen-qwq-32b"
        
        self.direct_agent = DirectAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.reasoning_agent = ReasoningAgent()
        self.memory_agent = MemoryAgent()
        self.rag_agent = RAGAgent()
        
        print("Team Agent initialized with 5 specialized agents")

    def _route_request(self, user_input: str) -> str:
        system_prompt = """You are a routing system for an AI team. Route requests to the most appropriate agent:

- direct: Simple calculations, basic facts, greetings, direct questions
- knowledge: Complex explanations, educational content, detailed information
- reasoning: Multi-step analysis, problem-solving, logical reasoning
- memory: Personal information storage/retrieval, remember/recall requests
- rag: Knowledge base queries, document search, research questions

Respond with only one word: direct, knowledge, reasoning, memory, or rag"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.1,
                max_tokens=10
            )
            
            route = response.choices[0].message.content.strip().lower()
            
            if route not in ['direct', 'knowledge', 'reasoning', 'memory', 'rag']:
                route = 'direct'
            
            return route
            
        except Exception as e:
            print(f"Routing failed: {e}")
            return 'direct'

    def process(self, user_input: str) -> Dict[str, Any]:
        try:
            route = self._route_request(user_input)
            
            if route == 'direct':
                result = self.direct_agent.process(user_input)
            elif route == 'knowledge':
                result = self.knowledge_agent.process(user_input)
            elif route == 'reasoning':
                result = self.reasoning_agent.process(user_input)
            elif route == 'memory':
                result = self.memory_agent.process(user_input)
            elif route == 'rag':
                result = self.rag_agent.process(user_input)
            else:
                result = self.direct_agent.process(user_input)
            
            if isinstance(result, dict):
                result['route'] = route
            
            return result
            
        except Exception as e:
            return {
                "response": f"System error: {str(e)}",
                "agent": "team",
                "error": True
            }

    def get_system_stats(self) -> Dict[str, Any]:
        try:
            memory_stats = self.memory_agent.get_memory_stats()
            rag_stats = self.rag_agent.get_knowledge_stats()
            
            return {
                "system": "Agentic AI System",
                "user_context": "Mann Gupta - Bangalore",
                "agents": {
                    "direct": "Ready",
                    "knowledge": "Ready",
                    "reasoning": "Ready",
                    "memory": f"{memory_stats.get('total_memories', 0)} memories",
                    "rag": f"{rag_stats.get('total_documents', 0)} documents"
                },
                "memory_categories": memory_stats.get('categories', {}),
                "knowledge_categories": rag_stats.get('categories', {})
            }
        except Exception as e:
            return {"error": f"Stats retrieval failed: {e}"} 