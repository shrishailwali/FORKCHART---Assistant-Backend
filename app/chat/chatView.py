from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.postgresql import get_db
from app.chat.chatSchema import CreateChatRequest, ChatResponse, Message, BranchRequest, UpdateChatRequest
from app.chat.chat_service import create_chat as create_chat_service, get_chat_service, update_chat_service, delete_chat_service
from app.chat.chatModel import Chat, ChatType
from db.mongodb import chat_collection
from app.main import decodeJWT

router = APIRouter(prefix="/api/v1/chats", tags=["Chats"])


@router.post("/create-chat")
async def create_chat(payload: CreateChatRequest, token: dict = Depends(decodeJWT),db: Session = Depends(get_db)):
    """
    Create a new chat session.

    - Stores metadata in PostgreSQL.
    - Initializes an empty qa_pairs array in MongoDB.
    """
    try:
        chat = create_chat_service(db=db, request=payload)
        await chat_collection.chat_contents.insert_one({
            "chat_id": str(chat.chat_id),
            "qa_pairs": []
        })
        return {"chat_id": str(chat.chat_id), "message": "Chat created successfully"}
    except Exception as e:
        print(f"Error creating chat: {e}")
        raise HTTPException(status_code=500, detail="Failed to create chat")

@router.get("/get-chat")
async def get_chat(user_data: dict = Depends(decodeJWT), db: Session = Depends(get_db)):
    """
    Retrieve all chats for a given account_id including chat metadata and associated messages.
    """
    try:
        account_id = user_data.get("account_id")
        chats = get_chat_service(db=db, account_id=str(account_id))
        if not chats:
            raise HTTPException(status_code=404, detail="No chats found")
        
        chat_messages = []
        for chat in chats:
            mongo_chat = await chat_collection.chat_contents.find_one({"chat_id": str(chat.chat_id)})
            chat_messages.append({
                "chat_id": str(chat.chat_id),
                "name": chat.name,
                "chat_type": chat.chat_type,
                "created_at": chat.created_at,
                "updated_at": chat.updated_at,
                "qa_pairs": mongo_chat["qa_pairs"] if mongo_chat else []
            })

        return chat_messages
    except Exception as e:
        print(f"Error retrieving chats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chats")


@router.put("/update-chat")
async def update_chat(payload: UpdateChatRequest, user_data: dict = Depends(decodeJWT), db: Session = Depends(get_db)):
    """
    Update the name and type of an existing chat.
    """
    try:
        account_id = user_data.get("account_id")
        updated_chat = update_chat_service(db=db, request=payload)
        if not updated_chat:
            raise HTTPException(status_code=404, detail="Chat not found or inactive")
        return {"message": "Chat updated successfully", "chat_id": str(updated_chat.chat_id)}
    except Exception as e:
        print(f"Error updating chat: {e}")
        raise HTTPException(status_code=500, detail="Failed to update chat")


@router.delete("/delete-chat")
async def delete_chat(account_id: str, user_data: dict = Depends(decodeJWT), db: Session = Depends(get_db)):
    """
    Delete a chat using account_id.
    
    - Removes metadata from PostgreSQL.
    - Deletes messages from MongoDB.
    """
    try:
        account_id = user_data.get("account_id")
        deleted = delete_chat_service(db=db, account_id=account_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Chat not found or already deleted")
        
        await chat_collection.chat_contents.delete_one({"chat_id": str(deleted.chat_id)})
        return {"message": "Chat deleted successfully", "chat_id": str(deleted.chat_id)}
    except Exception as e:
        print(f"Error deleting chat: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete chat")


@router.post("/add-message")
async def add_message(msg: Message):
    """
    Add a new QA pair (question and response) to an existing chat.
    
    - Stores the message in MongoDB.
    """
    try:
        chat = await chat_collection.chat_contents.find_one({"chat_id": str(msg.chat_id)})
        if not chat:
            return {"error": "Chat not found"}
        msg_dict = {
            "question": msg.question,
            "response": msg.response,
            "response_id": msg.response_id or str(uuid4()),
            "timestamp": msg.timestamp or datetime.utcnow(),
            "branches": []
        }
        await chat_collection.chat_contents.update_one(
            {"chat_id": str(msg.chat_id)},
            {"$push": {"qa_pairs": msg_dict}}
        )
        return {"message": "Message added successfully", "response_id": msg_dict["response_id"]}
    except Exception as e:
        print(f"Error adding message: {e}")
        return {"error": "Failed to add message"}


@router.post("/create-branch")
async def create_branch(payload: BranchRequest, db: Session = Depends(get_db)):
    """
    Create a branch of an existing chat from a specific response ID.

    - Copies all QA pairs up to the given response ID into a new chat.
    - Stores branch info in both PostgreSQL and MongoDB.
    """
    try:
        parent_chat = await chat_collection.chat_contents.find_one({"chat_id": str(payload.parent_chat_id)})
        if not parent_chat:
            return {"error": "Parent chat not found"}

        branch_chat_id = uuid4()
        new_qa_pairs = []

        for qa in parent_chat['qa_pairs']:
            new_qa_pairs.append(qa)
            if qa['response_id'] == payload.response_id:
                break

        await chat_collection.chat_contents.insert_one({
            "chat_id": str(branch_chat_id),
            "qa_pairs": new_qa_pairs
        })

        await chat_collection.chat_contents.update_one(
            {"chat_id": str(payload.parent_chat_id), "qa_pairs.response_id": payload.response_id},
            {"$push": {"qa_pairs.$.branches": str(branch_chat_id)}}
        )

        chat = Chat(
            chat_id=branch_chat_id,
            account_id=payload.account_id,
            name=payload.name,
            chat_type=ChatType.branched,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(chat)
        db.commit()
        return {"branch_chat_id": str(branch_chat_id), "message": "Branch created"}
    except Exception as e:
        print(f"Error creating branch: {e}")
        return {"error": "Failed to create branch"}
