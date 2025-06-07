from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class ChatInteraction(Base):
    __tablename__ = 'chat_interactions'
    
    id = Column(Integer, primary_key=True)
    user_input = Column(String, nullable=False)
    chosen_agent = Column(String, nullable=False)
    response = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatInteraction(id={self.id}, agent={self.chosen_agent})>" 