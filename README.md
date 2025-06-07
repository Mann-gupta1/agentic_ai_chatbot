# Agentic AI System

A multi-agent AI system with specialized agents for different types of tasks. Built for software professionals and tech enthusiasts.

## Features

- **Direct Agent**: Simple calculations and basic queries
- **Knowledge Agent**: Complex explanations and educational content  
- **Reasoning Agent**: Multi-step analysis and problem-solving
- **Memory Agent**: Personal information storage with vector similarity
- **RAG Agent**: Knowledge base retrieval with TF-IDF vectorization

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd agentic-ai
```

2. Install required dependencies:
```bash
pip install groq python-dotenv scikit-learn numpy
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

4. Initialize the system:
```bash
python setup_mann_gupta_context.py
```

## Usage

Run the interactive CLI:
```bash
python app.py
```

### Example Interactions

**Memory Storage:**
```
You: My name is Mann Gupta and I work as a software engineer
AI: I'll remember that information about you.
```

**Knowledge Queries:**
```
You: Tell me about Python programming
AI: Python is a high-level programming language...
```

**Calculations:**
```
You: What is 15 * 23?
AI: 15 * 23 = 345
```

**Reasoning:**
```
You: Should I learn machine learning?
AI: Based on current tech trends, machine learning offers...
```

## Architecture

The system uses a routing mechanism to direct queries to appropriate agents:

- **Team Agent**: Routes requests based on content analysis
- **Vector Storage**: TF-IDF with cosine similarity for memory/knowledge retrieval
- **Persistent Storage**: Pickle-based data persistence
- **Advanced ML**: SVD dimensionality reduction and clustering

## System Requirements

- Python 3.8+
- GROQ API key
- 500MB disk space for vector storage
- Internet connection for API calls

## Configuration

The system automatically creates:
- `memory_store_advanced.pkl` - Personal memory storage
- `knowledge_base_advanced.pkl` - Knowledge documents

## Testing

Run comprehensive tests:
```bash
# Test individual components
python -c "from agents.agent4_memory import MemoryAgent; agent = MemoryAgent(); print('Memory agent working')"

# Test system integration  
python -c "from agents.team_agent import TeamAgent; team = TeamAgent(); result = team.process('Hello'); print(result)"
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with clean, documented code
4. Test thoroughly
5. Submit pull request

## License

This project is for educational and demonstration purposes. 