"""
QA Chat Service
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.qa.daos.conversation_dao import ConversationDAO
from app.modules.qa.daos.message_dao import MessageDAO
from app.modules.qa.models.conversation import Conversation
from app.modules.qa.models.message import Message
from app.modules.qa.schemas.chat_schema import ChatCreate, ChatFeatures, MessageCreate
from app.modules.qa.agents.qa_agent import QAAgent


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.conversation_dao = ConversationDAO(db)
        self.message_dao = MessageDAO(db)
        self._agent: Optional[QAAgent] = None

    def _get_agent(self, use_rag: bool = True) -> QAAgent:
        """Get or create QA agent"""
        if self._agent is None:
            self._agent = QAAgent(
                provider="minimax",
                temperature=0.7,
                enable_rag=use_rag,
                top_k=4
            )
        return self._agent

    async def create_session(self, user_id: int, data: ChatCreate) -> Conversation:
        features_json = None
        if data.features:
            features_json = data.features.model_dump_json()

        conversation = Conversation(
            user_id=user_id,
            title=data.title or "新对话",
            features_json=features_json
        )
        return await self.conversation_dao.create(conversation)

    async def list_sessions(
        self,
        user_id: int,
        page: int = 1,
        size: int = 20
    ) -> List[Conversation]:
        offset = max(page - 1, 0) * size
        return await self.conversation_dao.list_by_user(
            user_id=user_id,
            offset=offset,
            limit=size
        )

    async def count_sessions(self, user_id: int) -> int:
        return await self.conversation_dao.count_by_user(user_id)

    async def get_session(self, user_id: int, session_id: int) -> Optional[Conversation]:
        return await self.conversation_dao.get_by_id(session_id, user_id)

    async def list_messages(
        self,
        user_id: int,
        session_id: int,
        page: int = 1,
        size: int = 50
    ) -> List[Message]:
        session = await self.get_session(user_id, session_id)
        if not session:
            return []
        offset = max(page - 1, 0) * size
        return await self.message_dao.list_by_conversation(
            conversation_id=session_id,
            offset=offset,
            limit=size
        )

    async def count_messages(self, user_id: int, session_id: int) -> int:
        session = await self.get_session(user_id, session_id)
        if not session:
            return 0
        return await self.message_dao.count_by_conversation(session_id)

    async def send_message(self, user_id: int, data: MessageCreate) -> Message:
        session = await self.get_session(user_id, data.session_id)
        if not session:
            raise ValueError("Session not found")

        user_message = Message(
            conversation_id=session.id,
            role="user",
            content=data.content,
            message_type=data.message_type
        )
        await self.message_dao.create(user_message)

        features = self.parse_features(session.features_json)
        use_rag = features.knowledge_base if features else True
        agent = self._get_agent(use_rag=use_rag)

        history_messages = await self.message_dao.list_by_conversation(
            conversation_id=session.id,
            offset=0,
            limit=10
        )
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in history_messages
        ]

        assistant_content = await agent.chat_with_history(data.content, history, use_rag=use_rag)
        assistant_message = Message(
            conversation_id=session.id,
            role="assistant",
            content=assistant_content,
            message_type="text"
        )
        return await self.message_dao.create(assistant_message)

    def _user_message_constructor(self, content: str, message_type: str, conversation_id: int) -> Message:
        """创建用户消息对象（用于流式接口）"""
        return Message(
            conversation_id=conversation_id,
            role="user",
            content=content,
            message_type=message_type
        )

    def _assistant_message_constructor(self, content: str, conversation_id: int) -> Message:
        """创建助手消息对象（用于流式接口）"""
        return Message(
            conversation_id=conversation_id,
            role="assistant",
            content=content,
            message_type="text"
        )

    async def _build_response(self, features_json: Optional[str], content: str) -> str:
        features = self.parse_features(features_json)
        use_rag = features.knowledge_base if features else True
        agent = self._get_agent(use_rag=use_rag)
        return await agent.chat(content, use_rag=use_rag)

    def parse_features(self, features_json: Optional[str]) -> Optional[ChatFeatures]:
        if not features_json:
            return None
        return ChatFeatures.model_validate_json(features_json)

    def mock_speech_to_text(self) -> dict:
        return {"text": "帮我查询一下北京的天气"}

    def mock_text_to_speech(self, text: str) -> dict:
        return {"audio_url": "https://example.com/audio/mock.mp3", "duration": 3.5}
