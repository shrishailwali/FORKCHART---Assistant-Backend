from sqlalchemy import Column, String, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import enum
import uuid
from datetime import datetime

Base = declarative_base()


class ChatType(str, enum.Enum):
    normal = "normal"
    branched = "branched"


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    chat_type = Column(Enum(ChatType), default=ChatType.normal)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean, default=True)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.chat_id"))
    account_id = Column(String, nullable=False)
    name = Column(String, nullable=True)
    deleted = Column(Boolean, default=False)
