from typing import Dict, Any
from agents.team_agent import TeamAgent

class AgentWorkflow:
    """
    Workflow system that coordinates agent interactions
    """
    
    def __init__(self):
        self.team_agent = TeamAgent()
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user request through the workflow system
        """
        try:
            result = self.team_agent.process(user_input)
            result["workflow_processed"] = True
            result["agent_used"] = result.get("agent", "unknown")
            return result
        except Exception as e:
            return {
                "success": False,
                "response": f"Workflow error: {str(e)}",
                "workflow_processed": False,
                "agent_used": "none"
            } 