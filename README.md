# Agentic AI System

A multi-agent AI system with specialized agents for different types of tasks. 

## Features

- **Direct Agent**: Simple calculations and basic queries
- **Knowledge Agent**: Complex explanations and educational content  
- **Reasoning Agent**: Multi-step analysis and problem-solving
- **Memory Agent**: Personal information storage with vector similarity
- **RAG Agent**: Knowledge base retrieval with TF-IDF vectorization


## Getting Started (Windows)
### Installation
1. Clone or download this repository to your desired location
2. Create a virtual environment:
   ```powershell
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. Install required dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

### Configuration
1. **Get MCP Server Key:**
   - First, start the MCP server:
     ```powershell
     cd mcp-server
     python server.py
     ```
   - In a new PowerShell window, generate an API key:
     ```powershell
     curl -X POST http://localhost:8081/generate_api_key
     ```
   - Copy the generated `api_key` from the JSON response

2. Create a `.env` file in the root directory and add the following variables:
   ```env
   GROQ_API_KEY=your_groq_api_key
   DATABASE_URL=postgresql://admin:admin@localhost:5432/agentic_chat
   MCP_ENDPOINT=http://localhost:8081
   MCP_API_KEY=your_generated_api_key_here
   ```

### Running the System
1. Start the database server:
   ```powershell
   cd db
   docker-compose up -d
   ```

2. Run the MCP server:
   ```powershell
    cd mcp-server
    docker-compose up -d
   ```

3. Run the UI application:
   ```powershell
   streamlit run app.py
   ```

## Architecture

The system uses a routing mechanism to direct queries to appropriate agents:

- **Team Agent**: Routes requests based on content analysis
- **Vector Storage**: TF-IDF with cosine similarity for memory/knowledge retrieval
- **Persistent Storage**: Pickle-based data persistence
- **Advanced ML**: SVD dimensionality reduction and clustering

 