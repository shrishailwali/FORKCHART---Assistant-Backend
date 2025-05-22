from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid
import enum


class ChatType(str, enum.Enum):
    normal = "normal"
    branched = "branched"


class CreateChatRequest(BaseModel):
    account_id: str
    name: str
    chat_type: ChatType = ChatType.normal

class UpdateChatRequest(BaseModel):
    account_id: str
    name: Optional[str]
    chat_type: Optional[ChatType]


class ChatResponse(BaseModel):
    chat_id: uuid.UUID
    account_id: str
    name: str
    chat_type: ChatType
    created_at: datetime
    updated_at: datetime
    active: bool


class Message(BaseModel):
    chat_id: str
    question: str
    response: str
    response_id: Optional[str] = None
    timestamp: Optional[datetime] = None


class BranchRequest(BaseModel):
    parent_chat_id: uuid.UUID
    response_id: str
    account_id: str
    name: str


