import os
from dotenv import load_dotenv
from agents.agent4_memory import MemoryAgent
from agents.agent5_rag import RAGAgent

load_dotenv()

def setup_personal_memories():
    print("Setting up personal memories for Mann Gupta...")
    
    memory_agent = MemoryAgent()
    
    personal_memories = [
        "My name is Mann Gupta and I live in Bangalore, India",
        "I work as a software engineer in the tech industry",
        "I am interested in artificial intelligence and machine learning",
        "I prefer Python programming language for development",
        "I live in Bangalore, which is known as India's Silicon Valley",
        "I enjoy working on AI and automation projects",
        "I am familiar with data science and programming",
        "I like to stay updated with latest technology trends",
        "I work in the Indian tech ecosystem",
        "I have experience with software development best practices"
    ]
    
    for memory in personal_memories:
        memory_agent._store_memory(memory, "personal_setup", importance=0.9)
    
    print(f"Added {len(personal_memories)} personal memories")
    return memory_agent.get_memory_stats()

def setup_knowledge_base():
    print("Setting up knowledge base with tech content...")
    
    rag_agent = RAGAgent()
    
    additional_knowledge = [
        {
            "title": "Bangalore Tech Hub",
            "content": "Bangalore is India's Silicon Valley, home to major tech companies, startups, and IT services. The city has a thriving tech ecosystem with numerous multinational corporations and innovative startups.",
            "category": "tech",
            "tags": ["bangalore", "india", "tech hub", "silicon valley"]
        },
        {
            "title": "Python in Data Science",
            "content": "Python is widely used in data science due to libraries like pandas, numpy, scikit-learn, and tensorflow. It's preferred for machine learning, data analysis, and AI development.",
            "category": "programming",
            "tags": ["python", "data science", "machine learning", "ai"]
        },
        {
            "title": "Software Engineering Best Practices",
            "content": "Modern software engineering involves agile methodologies, continuous integration, code reviews, testing, and documentation. These practices ensure quality and maintainable code.",
            "category": "software",
            "tags": ["software engineering", "best practices", "agile", "testing"]
        }
    ]
    
    for knowledge in additional_knowledge:
        rag_agent.add_knowledge(
            title=knowledge["title"],
            content=knowledge["content"],
            category=knowledge["category"],
            tags=knowledge["tags"]
        )
    
    print(f"Added {len(additional_knowledge)} knowledge documents")
    return rag_agent.get_knowledge_stats()

def main():
    print("Mann Gupta Context Setup")
    print("Setting up personalized AI system")
    print("-" * 40)
    
    try:
        memory_stats = setup_personal_memories()
        print(f"Memory setup complete: {memory_stats['total_memories']} memories")
        
        knowledge_stats = setup_knowledge_base()
        print(f"Knowledge base setup complete: {knowledge_stats['total_documents']} documents")
        
        print("\nSetup completed successfully!")
        print("You can now run the main application with: python app.py")
        
    except Exception as e:
        print(f"Setup failed: {e}")

if __name__ == "__main__":
    main() 