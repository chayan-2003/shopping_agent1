from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import CheckoutRequest, OrderHistoryOut, OrderOut
from app.services.order_service import checkout, get_order_history

router = APIRouter(tags=["orders"])


@router.post("/checkout/{session_id}", response_model=OrderOut)
def checkout_cart(session_id: str, body: CheckoutRequest, db: Session = Depends(get_db)) -> OrderOut:
    try:
        result = checkout(db, session_id=session_id, shipping_address=body.shipping_address)
        return OrderOut.model_validate(result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/orders/{session_id}", response_model=OrderHistoryOut)
def get_orders(session_id: str, db: Session = Depends(get_db)) -> OrderHistoryOut:
    orders = get_order_history(db, session_id=session_id)
    return OrderHistoryOut(orders=[OrderOut.model_validate(order) for order in orders])
