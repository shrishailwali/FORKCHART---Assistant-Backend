from databases import Database
from sqlmodel import SQLModel, create_engine
# from app.chat.chatModel import Base

MONGO_DATABASE_URL = "mongodb://localhost:27017"
SQLALCHEMY_DATABASE = "postgresql://postgres:postgres@localhost:5432/forkchat"
database = Database(SQLALCHEMY_DATABASE)
engine = create_engine(SQLALCHEMY_DATABASE, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)