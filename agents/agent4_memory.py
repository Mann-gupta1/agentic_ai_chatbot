from typing import Dict, Any, List
from groq import Groq
import os
import pickle
import numpy as np
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MemoryAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=api_key)
        self.model = "qwen-qwq-32b"
        
        self.memory_store = []
        self.vectorizer = TfidfVectorizer(
            max_features=2000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.memory_vectors = None
        self.memory_file = "memory_store_advanced.pkl"
        
        # Simple categories
        self.memory_categories = {
            'personal': ['name', 'mann', 'gupta', 'bangalore', 'india', 'age'],
            'work': ['job', 'work', 'programming', 'software', 'tech', 'coding'],
            'preferences': ['like', 'prefer', 'favorite', 'enjoy', 'python'],
            'general': ['other', 'misc', 'information']
        }
        
        self._load_memory()
        
    def _load_memory(self):
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'rb') as f:
                    data = pickle.load(f)
                    self.memory_store = data.get('memories', [])
                    if self.memory_store:
                        texts = [mem['content'] for mem in self.memory_store]
                        self.memory_vectors = self.vectorizer.fit_transform(texts)
                        print(f"Loaded {len(self.memory_store)} memories")
        except Exception as e:
            print(f"Memory loading failed: {e}")
            self.memory_store = []
            self.memory_vectors = None
    
    def _save_memory(self):
        try:
            data = {'memories': self.memory_store}
            with open(self.memory_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Memory saving failed: {e}")
    
    def _categorize_memory(self, content: str) -> str:
        content_lower = content.lower()
        category_scores = {}
        
        for category, keywords in self.memory_categories.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                category_scores[category] = score
        
        return max(category_scores, key=category_scores.get) if category_scores else 'general'
    
    def _calculate_importance(self, content: str, context: str = "") -> float:
        importance = 0.5
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['mann gupta', 'bangalore', 'my name']):
            importance += 0.4
            
        if any(word in content_lower for word in ['python', 'programming', 'tech']):
            importance += 0.2
            
        if len(content) > 50:
            importance += 0.1
            
        return min(importance, 1.0)
    
    def _store_memory(self, content: str, context: str = "", importance: float = None):
        if importance is None:
            importance = self._calculate_importance(content, context)
        
        category = self._categorize_memory(content)
        
        memory_entry = {
            'content': content,
            'context': context,
            'category': category,
            'timestamp': datetime.now().isoformat(),
            'importance': importance,
            'access_count': 0,
            'last_accessed': None
        }
        
        self.memory_store.append(memory_entry)
        
        texts = [mem['content'] for mem in self.memory_store]
        self.memory_vectors = self.vectorizer.fit_transform(texts)
        
        self._save_memory()
        print(f"Stored memory: {content[:50]}...")
    
    def _retrieve_relevant_memories(self, query: str, top_k: int = 5) -> List[Dict]:
        if not self.memory_store or self.memory_vectors is None:
            return []
        
        try:
            query_vector = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vector, self.memory_vectors)[0]
            similarity_indices = np.argsort(similarities)[::-1]
            
            relevant_memories = []
            for idx in similarity_indices[:top_k]:
                similarity_score = similarities[idx]
                
                if similarity_score > 0.1:
                    memory = self.memory_store[idx].copy()
                    memory['similarity'] = similarity_score
                    memory['index'] = idx
                    relevant_memories.append(memory)
            
            for mem in relevant_memories:
                idx = mem['index']
                self.memory_store[idx]['access_count'] += 1
                self.memory_store[idx]['last_accessed'] = datetime.now().isoformat()
            
            return relevant_memories
            
        except Exception as e:
            print(f"Memory retrieval failed: {e}")
            return []

    def process(self, user_input: str) -> Dict[str, Any]:
        try:
            relevant_memories = self._retrieve_relevant_memories(user_input)
            
            memory_context = ""
            if relevant_memories:
                memory_context = "\nRelevant memories:\n"
                for i, mem in enumerate(relevant_memories):
                    memory_context += f"{i+1}. {mem['content']}\n"
            
            # Check for memory storage requests
            memory_triggers = ['remember', 'my name', 'i am', 'i live', 'i work', 'i like']
            should_store = any(trigger in user_input.lower() for trigger in memory_triggers)
            
            if should_store:
                self._store_memory(user_input, "user_statement")
            
            system_prompt = f"""You are a personal memory assistant for Mann Gupta in Bangalore, India.
{memory_context}
Respond naturally about stored information. If storing new information, confirm what you've learned.
User input: {user_input}
"""
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            if len(self.memory_store) > 100:
                self._clean_old_memories()
            
            return {
                "response": response.choices[0].message.content,
                "agent": "memory",
                "memories_used": len(relevant_memories)
            }
            
        except Exception as e:
            return {"response": f"Memory processing failed: {str(e)}", "agent": "memory", "error": True}

    def _clean_old_memories(self):
        if len(self.memory_store) <= 100:
            return
        
        for memory in self.memory_store:
            age_days = (datetime.now() - datetime.fromisoformat(memory['timestamp'])).days
            access_score = memory.get('access_count', 0) * 0.1
            importance_score = memory.get('importance', 0.5)
            recency_score = max(0, 1 - age_days / 365)
            
            memory['retention_score'] = (importance_score * 0.5 + 
                                       access_score * 0.3 + 
                                       recency_score * 0.2)
        
        self.memory_store.sort(key=lambda x: x['retention_score'], reverse=True)
        self.memory_store = self.memory_store[:100]
        
        if self.memory_store:
            texts = [mem['content'] for mem in self.memory_store]
            self.memory_vectors = self.vectorizer.fit_transform(texts)
        
        self._save_memory()
        print("Cleaned old memories")

    def get_memory_stats(self) -> Dict[str, Any]:
        if not self.memory_store:
            return {"total_memories": 0, "categories": {}}
        
        categories = {}
        for memory in self.memory_store:
            category = memory.get('category', 'general')
            categories[category] = categories.get(category, 0) + 1
        
        avg_importance = np.mean([mem.get('importance', 0.5) for mem in self.memory_store])
        
        return {
            "total_memories": len(self.memory_store),
            "categories": categories,
            "average_importance": avg_importance
        }
