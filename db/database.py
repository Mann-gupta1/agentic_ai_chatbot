from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .models import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/agentic_chat")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_interaction(user_input: str, chosen_agent: str, response: str):
    from .models import ChatInteraction
    
    db = SessionLocal()
    try:
        interaction = ChatInteraction(
            user_input=user_input,
            chosen_agent=chosen_agent,
            response=response
        )
        db.add(interaction)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error saving interaction: {str(e)}")
        return False
    finally:
        db.close() 