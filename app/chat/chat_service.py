from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List, Optional

from app.chat.chatModel import Chat
from app.chat.chatSchema import CreateChatRequest, UpdateChatRequest


def create_chat(db: Session, request: CreateChatRequest) -> Chat:
    """Create a new chat."""
    new_chat = Chat(
        chat_id=uuid4(),
        account_id=request.account_id,
        name=request.name,
        chat_type=request.chat_type
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


def get_chat_service(db: Session, account_id: str) -> List[Chat]:
    """Retrieve all chats for a given account_id."""
    return db.query(Chat).filter(Chat.account_id == account_id, Chat.active == True).all()


def update_chat_service(db: Session, request: UpdateChatRequest) -> Optional[Chat]:
    """Update the name or chat_type for a chat belonging to an account."""
    chat = db.query(Chat).filter(Chat.account_id == request.account_id, Chat.active == True).first()
    if chat:
        if request.name:
            chat.name = request.name
        if request.chat_type:
            chat.chat_type = request.chat_type
        db.commit()
        db.refresh(chat)
    return chat


def delete_chat_service(db: Session, account_id: str) -> Optional[Chat]:
    """Soft delete: Set chat.active = False instead of physical deletion."""
    chat = db.query(Chat).filter(Chat.account_id == account_id, Chat.active == True).first()
    if chat:
        chat.active = False  # Soft delete
        db.commit()
        db.refresh(chat)
    return chat
