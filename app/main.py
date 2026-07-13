from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.ai.assistant import assistant
from app.database import Base, engine, get_db
from app.schemas import (
    CartAddRequest,
    CartOut,
    ChatRequest,
    ChatResponse,
    CheckoutRequest,
    OrderOut,
    OrderHistoryOut,
    ProductOut,
)
from app.seed import seed_products_if_empty
from app.services.cart_service import add_item_to_cart, get_cart_summary, remove_item_from_cart
from app.services.catalog_service import search_products
from app.services.order_service import checkout, get_order_history

app = FastAPI(title="Shopping AI Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        seed_products_if_empty(db)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products", response_model=list[ProductOut])
def list_products(
    query: str | None = None,
    category: str | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db),
) -> list[ProductOut]:
    products = search_products(db, query=query, category=category, max_price=max_price)
    return [ProductOut.model_validate(p) for p in products]


@app.get("/cart/{session_id}", response_model=CartOut)
def get_cart(session_id: str, db: Session = Depends(get_db)) -> CartOut:
    return CartOut.model_validate(get_cart_summary(db, session_id))


@app.post("/cart/{session_id}/items", response_model=CartOut)
def add_cart_item(session_id: str, body: CartAddRequest, db: Session = Depends(get_db)) -> CartOut:
    try:
        summary = add_item_to_cart(db, session_id=session_id, product_id=body.product_id, quantity=body.quantity)
        return CartOut.model_validate(summary)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.delete("/cart/{session_id}/items/{product_id}", response_model=CartOut)
def remove_cart_item(session_id: str, product_id: int, db: Session = Depends(get_db)) -> CartOut:
    summary = remove_item_from_cart(db, session_id=session_id, product_id=product_id)
    return CartOut.model_validate(summary)


@app.post("/checkout/{session_id}", response_model=OrderOut)
def checkout_cart(session_id: str, body: CheckoutRequest, db: Session = Depends(get_db)) -> OrderOut:
    try:
        result = checkout(db, session_id=session_id, shipping_address=body.shipping_address)
        return OrderOut.model_validate(result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/orders/{session_id}", response_model=OrderHistoryOut)
def get_orders(session_id: str, db: Session = Depends(get_db)) -> OrderHistoryOut:
    orders = get_order_history(db, session_id=session_id)
    return OrderHistoryOut(orders=[OrderOut.model_validate(order) for order in orders])


@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    try:
        reply = assistant.chat(db=db, session_id=body.session_id, message=body.message)
        return ChatResponse(session_id=body.session_id, reply=reply)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Assistant error: {exc}") from exc
