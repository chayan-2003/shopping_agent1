from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import CartAddRequest, CartOut
from app.services.cart_service import add_item_to_cart, get_cart_summary, remove_item_from_cart

router = APIRouter(tags=["cart"])


@router.get("/cart/{session_id}", response_model=CartOut)
def get_cart(session_id: str, db: Session = Depends(get_db)) -> CartOut:
    return CartOut.model_validate(get_cart_summary(db, session_id))


@router.post("/cart/{session_id}/items", response_model=CartOut)
def add_cart_item(session_id: str, body: CartAddRequest, db: Session = Depends(get_db)) -> CartOut:
    try:
        summary = add_item_to_cart(db, session_id=session_id, product_id=body.product_id, quantity=body.quantity)
        return CartOut.model_validate(summary)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/cart/{session_id}/items/{product_id}", response_model=CartOut)
def remove_cart_item(session_id: str, product_id: int, db: Session = Depends(get_db)) -> CartOut:
    summary = remove_item_from_cart(db, session_id=session_id, product_id=product_id)
    return CartOut.model_validate(summary)
