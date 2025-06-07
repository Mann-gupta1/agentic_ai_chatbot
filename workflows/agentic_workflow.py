from typing import Dict, Any
from agents.team_agent import TeamAgent
from db.database import save_interaction
from mcp.mcp_client import MCPClient

class AgenticWorkflow:
    def __init__(self):
        self.team_agent = TeamAgent()
        self.mcp_client = MCPClient()
        self.mcp_enabled = self._setup_mcp()

    def _setup_mcp(self) -> bool:
        try:
            if not self.mcp_client.is_server_available():
                print("MCP Server not available - running in standalone mode")
                return False
            
            print("MCP Server detected - setting up integration...")
            
            if not self.mcp_client.api_key:
                print("MCP_API_KEY not found in environment")
                print("Please run: python setup_mcp.py")
                return False
            agents_to_register = [
                {
                    "name": "direct_agent",
                    "type": "direct",
                    "description": "Handles simple, straightforward questions",
                    "capabilities": ["facts", "calculations", "definitions"]
                },
                {
                    "name": "knowledge_agent", 
                    "type": "knowledge",
                    "description": "Handles questions requiring expertise and detailed information",
                    "capabilities": ["research", "expertise", "detailed_explanations"]
                },
                {
                    "name": "reasoning_agent",
                    "type": "reasoning", 
                    "description": "Handles complex questions requiring memory and reasoning",
                    "capabilities": ["memory", "context", "multi_step_reasoning"]
                },
                {
                    "name": "memory_agent",
                    "type": "memory",
                    "description": "Handles personal information and conversation memory",
                    "capabilities": ["persistent_memory", "vector_storage", "personalization"]
                },
                {
                    "name": "rag_agent",
                    "type": "rag",
                    "description": "Handles knowledge retrieval and document-based responses",
                    "capabilities": ["document_retrieval", "vector_search", "knowledge_synthesis"]
                }
            ]
            
            registered_count = 0
            for agent_config in agents_to_register:
                result = self.mcp_client.register_agent(agent_config["name"], agent_config)
                if result["success"]:
                    print(f"Registered {agent_config['name']} with MCP")
                    registered_count += 1
                else:
                    print(f"Failed to register {agent_config['name']}: {result.get('error', 'Unknown error')}")
            
            print(f"MCP Integration complete - {registered_count}/5 agents registered")
            return registered_count > 0
            
        except Exception as e:
            print(f"MCP setup failed: {str(e)}")
            return False

    def process_query(self, user_input: str) -> Dict[str, Any]:
        try:
            result = self.team_agent.process(user_input)
            
            if self.mcp_enabled and result["success"]:
                agent_name = f"{result['chosen_agent']}_agent"
                mcp_data = {
                    "query": user_input,
                    "agent_type": result["chosen_agent"],
                    "local_response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
                }
                
                mcp_result = self.mcp_client.execute_agent(agent_name, mcp_data)
                if mcp_result["success"]:
                    result["mcp_logged"] = True
                    result["mcp_timestamp"] = mcp_result.get("timestamp")
                else:
                    result["mcp_logged"] = False
                    result["mcp_error"] = mcp_result.get("error")
            
            if result["success"]:
                save_interaction(
                    user_input=user_input,
                    chosen_agent=result["chosen_agent"],
                    response=result["response"]
                )
            
            return {
                "success": result["success"],
                "response": result["response"],
                "chosen_agent": result["chosen_agent"],
                "mcp_enabled": self.mcp_enabled,
                "mcp_logged": result.get("mcp_logged", False)
            }
            
        except Exception as e:
            error_response = f"Error in workflow processing: {str(e)}"
            
            save_interaction(
                user_input=user_input,
                chosen_agent="error",
                response=error_response
            )
            
            return {
                "success": False,
                "response": error_response,
                "chosen_agent": "error",
                "mcp_enabled": self.mcp_enabled,
                "mcp_logged": False
            } 