from typing import Dict, Any, List
from groq import Groq
import os
import pickle
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

class RAGAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=api_key)
        self.model = "qwen-qwq-32b"
        
        self.knowledge_store = []
        self.vectorizer = TfidfVectorizer(
            max_features=3000,
            stop_words='english',
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.9
        )
        self.knowledge_vectors = None
        self.svd = TruncatedSVD(n_components=100, random_state=42)
        self.reduced_vectors = None
        
        self.knowledge_file = "knowledge_base_advanced.pkl"
        
        self._initialize_knowledge_base()
        
    def _initialize_knowledge_base(self):
        try:
            if os.path.exists(self.knowledge_file):
                with open(self.knowledge_file, 'rb') as f:
                    data = pickle.load(f)
                    self.knowledge_store = data.get('knowledge', [])
                    if self.knowledge_store:
                        self._build_vectors()
                        print(f"Loaded {len(self.knowledge_store)} knowledge documents")
                        return
        except Exception as e:
            print(f"Knowledge loading failed: {e}")
        
        self._create_default_knowledge()
        
    def _create_default_knowledge(self):
        knowledge_base = [
            {
                "title": "Python Programming Basics",
                "content": "Python is a high-level programming language known for its simplicity and readability. It supports multiple paradigms including object-oriented, procedural, and functional programming. Python is widely used in web development, data science, artificial intelligence, and automation.",
                "category": "programming",
                "tags": ["python", "programming", "basics"]
            },
            {
                "title": "Machine Learning Fundamentals",
                "content": "Machine learning is a subset of artificial intelligence that enables computers to learn patterns from data without being explicitly programmed. It includes supervised learning, unsupervised learning, and reinforcement learning approaches.",
                "category": "ai",
                "tags": ["machine learning", "ai", "data science"]
            },
            {
                "title": "Software Development Best Practices",
                "content": "Good software development practices include writing clean code, using version control, testing thoroughly, documenting code, following design patterns, and maintaining code quality through code reviews.",
                "category": "software",
                "tags": ["software development", "best practices", "coding"]
            },
            {
                "title": "Technology in India",
                "content": "India has a thriving technology sector with major IT hubs in cities like Bangalore, Hyderabad, and Pune. The country is home to numerous global tech companies and startups, making it a significant player in the global technology landscape.",
                "category": "tech",
                "tags": ["india", "technology", "bangalore", "it"]
            },
            {
                "title": "Data Structures and Algorithms",
                "content": "Data structures organize and store data efficiently, while algorithms are step-by-step procedures for solving problems. Common data structures include arrays, linked lists, trees, and graphs. Understanding these is crucial for programming interviews and efficient coding.",
                "category": "programming",
                "tags": ["data structures", "algorithms", "programming"]
            }
        ]
        
        for kb in knowledge_base:
            kb['id'] = f"kb_{len(self.knowledge_store) + 1}"
            kb['created_at'] = datetime.now().isoformat()
            kb['access_count'] = 0
            self.knowledge_store.append(kb)
        
        self._build_vectors()
        self._save_knowledge()
        print(f"Created knowledge base with {len(self.knowledge_store)} documents")
    
    def _build_vectors(self):
        if not self.knowledge_store:
            return
        
        texts = [f"{doc['title']} {doc['content']}" for doc in self.knowledge_store]
        self.knowledge_vectors = self.vectorizer.fit_transform(texts)
        
        if self.knowledge_vectors.shape[0] > 1:
            n_components = min(100, self.knowledge_vectors.shape[1], self.knowledge_vectors.shape[0])
            self.svd = TruncatedSVD(n_components=n_components, random_state=42)
            self.reduced_vectors = self.svd.fit_transform(self.knowledge_vectors)
        else:
            self.reduced_vectors = self.knowledge_vectors.toarray()
    
    def _save_knowledge(self):
        try:
            data = {'knowledge': self.knowledge_store}
            with open(self.knowledge_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Knowledge saving failed: {e}")
    
    def _retrieve_relevant_knowledge(self, query: str, top_k: int = 3) -> List[Dict]:
        if not self.knowledge_store or self.knowledge_vectors is None:
            return []
        
        try:
            query_vector = self.vectorizer.transform([query])
            
            if hasattr(self, 'reduced_vectors') and self.reduced_vectors is not None:
                query_reduced = self.svd.transform(query_vector)
                similarities = cosine_similarity(query_reduced, self.reduced_vectors)[0]
            else:
                similarities = cosine_similarity(query_vector, self.knowledge_vectors)[0]
            
            similarity_indices = np.argsort(similarities)[::-1]
            
            relevant_docs = []
            for idx in similarity_indices[:top_k]:
                similarity_score = similarities[idx]
                
                if similarity_score > 0.05:
                    doc = self.knowledge_store[idx].copy()
                    doc['similarity'] = similarity_score
                    doc['index'] = idx
                    relevant_docs.append(doc)
            
            for doc in relevant_docs:
                idx = doc['index']
                self.knowledge_store[idx]['access_count'] += 1
            
            return relevant_docs
            
        except Exception as e:
            print(f"Knowledge retrieval failed: {e}")
            return []
    
    def add_knowledge(self, title: str, content: str, category: str = "general", tags: List[str] = None):
        if tags is None:
            tags = []
        
        knowledge_doc = {
            'id': f"kb_{len(self.knowledge_store) + 1}",
            'title': title,
            'content': content,
            'category': category,
            'tags': tags,
            'created_at': datetime.now().isoformat(),
            'access_count': 0
        }
        
        self.knowledge_store.append(knowledge_doc)
        self._build_vectors()
        self._save_knowledge()
        print(f"Added knowledge: {title}")

    def process(self, user_input: str) -> Dict[str, Any]:
        try:
            relevant_docs = self._retrieve_relevant_knowledge(user_input)
            
            knowledge_context = ""
            if relevant_docs:
                knowledge_context = "\nRelevant knowledge:\n"
                for i, doc in enumerate(relevant_docs):
                    knowledge_context += f"{i+1}. {doc['title']}: {doc['content'][:200]}...\n"
            
            system_prompt = f"""You are a knowledge assistant for Mann Gupta in Bangalore, India.

{knowledge_context}

Use the knowledge base to provide comprehensive answers about programming, technology, and general topics.

User question: {user_input}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            return {
                "response": response.choices[0].message.content,
                "agent": "rag",
                "knowledge_docs_used": len(relevant_docs)
            }
            
        except Exception as e:
            return {"response": f"Knowledge retrieval failed: {str(e)}", "agent": "rag", "error": True}

    def get_knowledge_stats(self) -> Dict[str, Any]:
        if not self.knowledge_store:
            return {"total_documents": 0, "categories": {}}
        
        categories = {}
        for doc in self.knowledge_store:
            category = doc.get('category', 'general')
            categories[category] = categories.get(category, 0) + 1
        
        total_content_length = sum(len(doc['content']) for doc in self.knowledge_store)
        avg_content_length = total_content_length / len(self.knowledge_store)
        
        return {
            "total_documents": len(self.knowledge_store),
            "categories": categories,
            "average_content_length": avg_content_length,
            "vector_dimensions": self.knowledge_vectors.shape[1] if self.knowledge_vectors is not None else 0
        }
