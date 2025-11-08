"""
Chat API endpoints for RAG-powered conversations
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import ChatRequest, ChatResponse, ChatMessage
from database.supabase_client import supabase_client
from agents.rag_assistant import RAGQueryAssistantAgent
from app.core.logger import app_logger
from datetime import datetime
import uuid
import json

router = APIRouter()
rag_agent = RAGQueryAssistantAgent()


@router.post("/", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a chat message and get AI response"""
    try:
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # Get conversation history
        if request.conversation_id:
            conversations = await supabase_client.get_conversations("default_user")
            conversation = next((c for c in conversations if c["id"] == conversation_id), None)
            history = conversation.get("messages", []) if conversation else []
        else:
            history = []

        # Process query with RAG agent
        response = await rag_agent.execute({
            "query": request.message,
            "conversation_history": history,
            "context_ids": request.context_ids
        })

        # Prepare messages
        user_message = {
            "role": "user",
            "content": request.message,
            "timestamp": datetime.utcnow().isoformat()
        }

        assistant_message = {
            "role": "assistant",
            "content": response["content"],
            "timestamp": datetime.utcnow().isoformat()
        }

        updated_history = history + [user_message, assistant_message]

        # Save/update conversation
        if request.conversation_id:
            await supabase_client.update_conversation(
                conversation_id,
                {
                    "messages": json.dumps(updated_history),
                    "updated_at": datetime.utcnow().isoformat()
                }
            )
        else:
            await supabase_client.create_conversation({
                "id": conversation_id,
                "user_id": "default_user",
                "title": request.message[:100],
                "messages": json.dumps(updated_history),
                "context_ids": request.context_ids,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            })

        return ChatResponse(
            message=response["content"],
            conversation_id=conversation_id,
            sources=response.get("metadata", {}).get("sources", []),
            suggested_actions=response.get("metadata", {}).get("suggested_actions", [])
        )
    except Exception as e:
        app_logger.error(f"Error processing chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations")
async def get_conversations(user_id: str = "default_user", limit: int = 20):
    """Get user's conversation history"""
    try:
        conversations = await supabase_client.get_conversations(user_id)
        return conversations[:limit]
    except Exception as e:
        app_logger.error(f"Error fetching conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get a specific conversation"""
    try:
        conversations = await supabase_client.get_conversations("default_user")
        conversation = next((c for c in conversations if c["id"] == conversation_id), None)

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return conversation
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error fetching conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    try:
        # In a real implementation, would delete from database
        return {
            "message": "Conversation deleted",
            "conversation_id": conversation_id
        }
    except Exception as e:
        app_logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
