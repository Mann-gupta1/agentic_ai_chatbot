from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from typing import Dict, Any
import uvicorn
import secrets
import json
from datetime import datetime
import os
from pathlib import Path

app = FastAPI(title="Modular Control Plane")

# Setup API key handling
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Store for registered agents and their configurations
AGENTS_DB_FILE = "agents_db.json"

def load_agents_db():
    if Path(AGENTS_DB_FILE).exists():
        with open(AGENTS_DB_FILE, 'r') as f:
            return json.load(f)
    return {"agents": {}, "api_keys": {}}

def save_agents_db(db):
    with open(AGENTS_DB_FILE, 'w') as f:
        json.dump(db, f, indent=2)

# Initialize database
db = load_agents_db()

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in db["api_keys"]:
        return api_key_header
    raise HTTPException(
        status_code=403,
        detail="Invalid API Key"
    )

@app.post("/generate_api_key")
def generate_api_key():
    """Generate a new API key for accessing the MCP server."""
    api_key = secrets.token_urlsafe(32)
    db["api_keys"][api_key] = {
        "created_at": datetime.utcnow().isoformat(),
        "active": True
    }
    save_agents_db(db)
    return {"api_key": api_key}

@app.post("/register_agent")
def register_agent(agent_config: Dict[str, Any], api_key: str = Depends(get_api_key)):
    """Register a new agent with the MCP server."""
    agent_id = secrets.token_urlsafe(16)
    db["agents"][agent_id] = {
        "config": agent_config,
        "registered_at": datetime.utcnow().isoformat(),
        "status": "active"
    }
    save_agents_db(db)
    return {"agent_id": agent_id}

@app.post("/execute_agent/{agent_id}")
def execute_agent(agent_id: str, input_data: Dict[str, Any], api_key: str = Depends(get_api_key)):
    """Execute an agent with the given input data."""
    if agent_id not in db["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Mock execution - in reality, this would execute the agent's logic
    return {
        "success": True,
        "agent_id": agent_id,
        "result": f"Executed agent {agent_id} with input: {input_data}",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/agents")
def list_agents(api_key: str = Depends(get_api_key)):
    """List all registered agents."""
    return {"agents": list(db["agents"].keys())}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081) 