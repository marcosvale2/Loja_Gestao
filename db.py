from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
engine = create_engine('sqlite:///database.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
def init_db():
    import models
    Base.metadata.create_all(bind=engine)
