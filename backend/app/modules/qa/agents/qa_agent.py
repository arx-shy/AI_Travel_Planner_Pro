"""
QA Agent for chat functionality.

This module provides the intelligent agent for the QA system,
integrating with the LLM factory, RAG retriever, and prompt templates.
"""

from typing import List, Dict, Any, Optional
from app.core.ai.factory import LLMFactory
from app.modules.qa.rag.retriever import Retriever
from app.modules.qa.rag.knowledge_base import get_knowledge_base
from app.modules.qa.prompts.qa_prompts import (
    RAG_SYSTEM_PROMPT,
    GENERAL_SYSTEM_PROMPT,
    create_rag_prompt,
    create_general_prompt
)
from langchain_core.messages import HumanMessage, SystemMessage
import logging

logger = logging.getLogger(__name__)


class QAAgent:
    """
    QA Agent for handling chat interactions.
    
    This agent is responsible for:
    1. Retrieving relevant context using RAG
    2. Building prompts with retrieved context
    3. Generating responses using the LLM factory
    """

    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        enable_rag: bool = True,
        top_k: int = 4
    ):
        """
        Initialize QA Agent.
        
        Args:
            provider: AI provider (default uses OpenAI-compatible API)
            model_name: Model name
            temperature: Sampling temperature
            enable_rag: Whether to use RAG retrieval
            top_k: Number of top chunks to retrieve
        """
        try:
            self.llm_client = LLMFactory.create_client(
                provider=provider,
                model_name=model_name,
                temperature=temperature
            )
        except ValueError as e:
            logger.warning(f"LLM factory failed: {e}, using fallback mode")
            self.llm_client = None
            
        self.enable_rag = enable_rag
        self.top_k = top_k
        self._knowledge_base = None
        self._retriever = None

    def _get_knowledge_base(self):
        """Get or initialize knowledge base"""
        if self._knowledge_base is None:
            self._knowledge_base = get_knowledge_base()
        return self._knowledge_base

    def _get_retriever(self) -> Optional[Retriever]:
        """Get or initialize retriever"""
        if not self.enable_rag:
            return None
        if self._retriever is None:
            kb = self._get_knowledge_base()
            self._retriever = Retriever(kb._store) if kb and kb._store else None
        return self._retriever

    def _retrieve_context(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks for the query.
        
        Args:
            query: User's question
            
        Returns:
            List of retrieved chunks with metadata
        """
        retriever = self._get_retriever()
        if not retriever:
            return []
        
        try:
            chunks = retriever.retrieve(query, top_k=self.top_k)
            return [
                {
                    "content": chunk.content,
                    "source": chunk.source,
                    "page": chunk.page,
                    "chunk_id": chunk.chunk_id
                }
                for chunk in chunks
            ]
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return []

    def _build_messages(self, query: str, use_rag: bool = True) -> List[Any]:
        """
        Build message list for LLM.
        
        Args:
            query: User's question
            use_rag: Whether to include retrieved context
            
        Returns:
            List of LangChain messages
        """
        if use_rag:
            context_chunks = self._retrieve_context(query)
            if context_chunks:
                context = "\n\n".join([
                    f"[来源: {c['source']} 第{c['page']}页]\n{c['content']}"
                    for c in context_chunks
                ])
                return create_rag_prompt(query, context)
        
        return create_general_prompt(query)

    async def chat(self, query: str, use_rag: bool = True) -> str:
        """
        Generate response for user query.
        
        Args:
            query: User's question
            use_rag: Whether to use RAG retrieval
            
        Returns:
            Generated response text
        """
        try:
            messages = self._build_messages(query, use_rag)
            
            if self.llm_client is None:
                return self._fallback_response(query, use_rag)
            
            response = await LLMFactory.agenerate(self.llm_client, messages)
            
            if response:
                return response
            
            return self._fallback_response(query, use_rag)
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return self._fallback_response(query, use_rag)

    def _fallback_response(self, query: str, use_rag: bool) -> str:
        """
        Fallback response when LLM is unavailable.
        
        Args:
            query: User's question
            use_rag: Whether RAG was attempted
            
        Returns:
            Fallback response text
        """
        if use_rag:
            chunks = self._retrieve_context(query)
            if chunks:
                context = "\n\n".join([c['content'] for c in chunks[:2]])
                return (
                    f"我找到了以下相关信息：\n\n{context}\n\n"
                    f"关于您的问题「{query}」，建议参考以上资料。"
                )
        
        return (
            f"我理解您的问题是：「{query}」。\n\n"
            "我可以为您提供以下帮助：\n"
            "1. 行程规划建议 - 生成个性化的旅行计划\n"
            "2. 目的地信息 - 景点、美食、文化等\n"
            "3. 出行提示 - 天气、签证、交通等\n"
            "4. 文案生成 - 为社交媒体创建旅行文案\n\n"
            "请提供更多细节，我会尽力为您解答！"
        )

    async def chat_with_history(
        self,
        query: str,
        history: List[Dict[str, str]],
        use_rag: bool = True
    ) -> str:
        """
        Chat with conversation history support.
        
        Args:
            query: Current user query
            history: Conversation history (list of messages with role and content)
            use_rag: Whether to use RAG retrieval
            
        Returns:
            Generated response
        """
        try:
            messages = []
            
            if use_rag:
                context_chunks = self._retrieve_context(query)
                if context_chunks:
                    context = "\n\n".join([
                        f"[来源: {c['source']} 第{c['page']}页]\n{c['content']}"
                        for c in context_chunks
                    ])
                    messages.append(SystemMessage(content=RAG_SYSTEM_PROMPT))
                    messages.append(SystemMessage(content=f"参考资料：\n{context}"))
                else:
                    messages.append(SystemMessage(content=GENERAL_SYSTEM_PROMPT))
            else:
                messages.append(SystemMessage(content=GENERAL_SYSTEM_PROMPT))
            
            for msg in history[-10:]:
                if msg['role'] == 'user':
                    messages.append(HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    messages.append(SystemMessage(content=msg['content']))
            
            messages.append(HumanMessage(content=query))
            
            if self.llm_client is None:
                return self._fallback_response(query, use_rag)
            
            response = await LLMFactory.agenerate(self.llm_client, messages)
            return response or self._fallback_response(query, use_rag)
            
        except Exception as e:
            logger.error(f"Chat with history error: {e}")
            return self._fallback_response(query, use_rag)
