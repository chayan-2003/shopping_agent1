from collections import defaultdict

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.orm import Session

from app.ai.tools import build_tools
from app.core.config import settings


class ShoppingAssistant:
    def __init__(self) -> None:
        self._chat_history: dict[str, list] = defaultdict(list)

    def chat(self, db: Session, session_id: str, message: str) -> str:
        if not settings.google_api_key:
            return "GOOGLE_API_KEY is not configured. Add it to your environment or .env file."
        llm = ChatGoogleGenerativeAI(
            model=settings.google_model,
            google_api_key=settings.google_api_key,
            temperature=0.2,
        )
        tools = build_tools(db, session_id=session_id)

        history = self._chat_history[session_id]
        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=(
                "You are a shopping assistant. Help users discover products, manage carts, and place orders. "
                "Always use tools for product/cart/order data. Keep responses concise and action-oriented."
            ),
        )
        result = agent.invoke(
            {
                "messages": [*history, HumanMessage(content=message)],
            }
        )

        output = "I could not generate a response."
        messages = result.get("messages", [])
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                content = msg.content
                # Handle different response formats
                if isinstance(content, list):
                    # Extract text from structured response (filter out thinking blocks)
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            output = item.get('text', output)
                            break
                elif isinstance(content, str):
                    # Try to parse if it looks like a JSON list
                    import json
                    if content.strip().startswith('['):
                        try:
                            parsed = json.loads(content)
                            if isinstance(parsed, list):
                                for item in parsed:
                                    if isinstance(item, dict) and item.get('type') == 'text':
                                        output = item.get('text', output)
                                        break
                            else:
                                output = content
                        except (json.JSONDecodeError, ValueError):
                            output = content
                    else:
                        # Handle plain string content
                        output = content if content else "I could not generate a response."
                else:
                    # Handle other content types
                    output = str(content) if content else "I could not generate a response."
                break

        history.append(HumanMessage(content=message))
        history.append(AIMessage(content=output))
        return output


assistant = ShoppingAssistant()
