import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from config import DATABASE_URL

def get_db_connection():
    """Create a database connection"""
    try:
        conn = sqlite3.connect('./data/shipment_tracking.db')
        return conn
    except sqlite3.Error as e:
        raise Exception(f"Database connection error: {str(e)}")

# SQLAlchemy Engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session():
    """Get SQLAlchemy session"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def init_db():
    """Initialize database and create tables"""
    from .models import Base
    Base.metadata.create_all(bind=engine)

def execute_query(query: str, params: dict = None):
    """Execute raw SQL query"""
    with get_db_session() as session:
        result = session.execute(query, params or {})
        return result