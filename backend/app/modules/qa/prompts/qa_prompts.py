"""
QA prompt templates.
"""

RAG_SYSTEM_PROMPT = (
    "你是旅行问答助手，请基于提供的参考资料回答问题。"
    "如果资料不足，请说明缺失并给出可能的方向。"
)

GENERAL_SYSTEM_PROMPT = (
    "你是专业的旅行问答助手，请直接回答用户问题，"
    "给出具体、可操作的建议，回答保持简洁清晰。"
)

def create_rag_prompt(query: str, context: str):
    """
    Create RAG prompt with context.

    Args:
        query: User's question
        context: Retrieved context from knowledge base

    Returns:
        List of messages (SystemMessage and HumanMessage)
    """
    from langchain_core.messages import SystemMessage, HumanMessage

    user_content = f"""
参考资料：
{context}

用户问题：{query}

请基于以上参考资料回答用户的问题。如果参考资料中没有相关信息，
请说明你不知道，并给出一些实用的建议方向。
    """.strip()

    return [
        SystemMessage(content=RAG_SYSTEM_PROMPT),
        HumanMessage(content=user_content)
    ]

def create_general_prompt(query: str):
    """
    Create general prompt without RAG context.

    Args:
        query: User's question

    Returns:
        List of messages (SystemMessage and HumanMessage)
    """
    from langchain_core.messages import SystemMessage, HumanMessage

    user_content = f"""
用户问题：{query}

请给出简洁、实用的回答。如果问题涉及具体目的地，
请提供相关的景点、美食、交通等信息。
    """.strip()

    return [
        SystemMessage(content=GENERAL_SYSTEM_PROMPT),
        HumanMessage(content=user_content)
    ]

def create_weather_prompt(city: str):
    """
    Create weather query prompt.

    Args:
        city: City name

    Returns:
        Formatted prompt string
    """
    return f"请查询{city}的天气预报，包括未来3天的天气状况、温度、湿度等信息。"
