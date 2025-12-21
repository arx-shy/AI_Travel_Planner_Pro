"""
QA Module API Routes (v1)
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_active_user
from app.modules.qa.schemas.chat_schema import ChatCreate, ChatResponse, MessageCreate, MessageResponse
from app.modules.qa.services.chat_service import ChatService

router = APIRouter()


@router.post("/sessions", response_model=ChatResponse)
async def create_chat_session(
    chat_data: ChatCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    session = await service.create_session(current_user.id, chat_data)
    features = service.parse_features(session.features_json)
    return ChatResponse(
        id=session.id,
        title=session.title,
        features=features,
        created_at=session.created_at
    )


@router.get("/sessions", response_model=list[ChatResponse])
async def list_chat_sessions(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    sessions = await service.list_sessions(current_user.id)
    return [
        ChatResponse(
            id=session.id,
            title=session.title,
            features=service.parse_features(session.features_json),
            created_at=session.created_at
        )
        for session in sessions
    ]


@router.post("/messages", response_model=MessageResponse)
async def send_message(
    message_data: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    try:
        message = await service.send_message(current_user.id, message_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    return MessageResponse(
        id=message.id,
        session_id=message.conversation_id,
        role=message.role,
        content=message.content,
        message_type=message.message_type,
        created_at=message.created_at
    )


@router.get("/sessions/{session_id}/messages", response_model=list[MessageResponse])
async def get_chat_history(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    messages = await service.list_messages(current_user.id, session_id)
    return [
        MessageResponse(
            id=msg.id,
            session_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            message_type=msg.message_type,
            created_at=msg.created_at
        )
        for msg in messages
    ]


@router.get("/weather/{city}")
async def query_weather(
    city: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    return service.mock_weather(city)


@router.post("/speech-to-text")
async def speech_to_text(
    audio: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    return service.mock_speech_to_text()


@router.post("/text-to-speech")
async def text_to_speech(
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ChatService(db)
    text = payload.get("text", "")
    return service.mock_text_to_speech(text)
