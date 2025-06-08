# Agentic AI System

A multi-agent AI system with specialized agents for different types of tasks. 

## Features

- **Direct Agent**: Simple calculations and basic queries
- **Knowledge Agent**: Complex explanations and educational content  
- **Reasoning Agent**: Multi-step analysis and problem-solving
- **Memory Agent**: Personal information storage with vector similarity
- **RAG Agent**: Knowledge base retrieval with TF-IDF vectorization


## Architecture

The system uses a routing mechanism to direct queries to appropriate agents:

- **Team Agent**: Routes requests based on content analysis
- **Vector Storage**: TF-IDF with cosine similarity for memory/knowledge retrieval
- **Persistent Storage**: Pickle-based data persistence
- **Advanced ML**: SVD dimensionality reduction and clustering

 