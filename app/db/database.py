import os
from datetime import datetime
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv(key="DATABASE_URL")

engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class BaseModel(Base):  # type: ignore
    __abstract__ = True
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    create_at = Column(DateTime, default=lambda: datetime.now())
    update_at = Column(
        DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now()
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        raise e
    finally:
        db.close()
