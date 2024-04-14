import os
from typing import List
from sqlmodel import create_engine, SQLModel, Session, Field, ARRAY, JSON, Column


DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
# Shared properties
class ChunkBase(SQLModel):
    text: str = Field(unique=False)
    embedding: List[str] = Field(sa_column=Column(JSON))


class Chunk(ChunkBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session