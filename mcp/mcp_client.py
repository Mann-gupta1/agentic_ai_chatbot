from typing import Dict, Any
import os
import requests
import json

class MCPClient:
    def __init__(self):
        self.mcp_endpoint = os.getenv("MCP_ENDPOINT", "http://localhost:8081")
        self.api_key = os.getenv("MCP_API_KEY")
        self.headers = {}
        if self.api_key:
            self.headers["X-API-Key"] = self.api_key
            self.headers["Content-Type"] = "application/json"
        self.registered_agents = {}
        
    def generate_api_key(self) -> Dict[str, Any]:
        try:
            response = requests.post(f"{self.mcp_endpoint}/generate_api_key", timeout=10)
            if response.status_code == 200:
                data = response.json()
                api_key = data["api_key"]
                self.api_key = api_key
                self.headers = {
                    "X-API-Key": api_key,
                    "Content-Type": "application/json"
                }
                return {"success": True, "api_key": api_key}
            else:
                return {"success": False, "error": f"Failed to generate API key: {response.status_code} - {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Error generating API key: {str(e)}"}
    
    def register_agent(self, agent_name: str, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            return {"success": False, "error": "MCP_API_KEY not found in environment. Please run setup_mcp.py first."}
        
        try:
            response = requests.post(
                f"{self.mcp_endpoint}/register_agent",
                json=agent_config,
                headers=self.headers
            )
            if response.status_code == 200:
                agent_id = response.json()["agent_id"]
                self.registered_agents[agent_name] = agent_id
                return {
                    "success": True,
                    "message": f"Agent {agent_name} registered successfully",
                    "agent_id": agent_id
                }
            else:
                return {"success": False, "error": f"Registration failed: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": f"Error registering agent: {str(e)}"}
    
    def execute_agent(self, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            return {"success": False, "error": "MCP_API_KEY not found in environment"}
            
        if agent_name not in self.registered_agents:
            # Try to register the agent first
            agent_config = {
                "name": agent_name,
                "type": agent_name.replace("_agent", ""),
                "description": f"Auto-registered {agent_name}"
            }
            reg_result = self.register_agent(agent_name, agent_config)
            if not reg_result["success"]:
                return {"success": False, "error": f"Agent {agent_name} not registered and auto-registration failed: {reg_result.get('error')}"}
        
        agent_id = self.registered_agents[agent_name]
        
        try:
            response = requests.post(
                f"{self.mcp_endpoint}/execute_agent/{agent_id}",
                json=input_data,
                headers=self.headers
            )
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "message": f"Agent {agent_name} executed successfully",
                    "result": result["result"],
                    "timestamp": result["timestamp"]
                }
            else:
                return {"success": False, "error": f"Execution failed: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": f"Error executing agent: {str(e)}"}
    
    def list_agents(self) -> Dict[str, Any]:
        """List all registered agents."""
        try:
            response = requests.get(f"{self.mcp_endpoint}/agents", headers=self.headers)
            if response.status_code == 200:
                agents = response.json()["agents"]
                return {"success": True, "agents": agents}
            else:
                return {"success": False, "error": f"Failed to list agents: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": f"Error listing agents: {str(e)}"}
    
    def is_server_available(self) -> bool:
        """Check if MCP server is available."""
        try:
            response = requests.get(f"{self.mcp_endpoint}/docs", timeout=5)
            return response.status_code == 200
        except:
            return False 