from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.assistant import assistant
from app.db.session import get_db
from app.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    try:
        reply = assistant.chat(db=db, session_id=body.session_id, message=body.message)
        return ChatResponse(session_id=body.session_id, reply=reply)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Assistant error: {exc}") from exc
