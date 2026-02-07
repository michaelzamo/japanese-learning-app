from sqlalchemy import create_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Pour le moment, on utilise SQLite pour simplifier le démarrage dans Codespaces
# On pourra passer à PostgreSQL plus tard sans changer le code
SQLALCHEMY_DATABASE_URL = "sqlite:///./japanese_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
