from datetime import datetime

from pydantic import BaseModel, Field


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    category: str
    price: float
    stock: int

    model_config = {"from_attributes": True}


class CartAddRequest(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=20)


class CartItemOut(BaseModel):
    product_id: int
    name: str
    quantity: int
    unit_price: float
    line_total: float


class CartOut(BaseModel):
    session_id: str
    items: list[CartItemOut]
    total_items: int
    subtotal: float


class CheckoutRequest(BaseModel):
    shipping_address: str = Field(min_length=5, max_length=500)


class OrderItemOut(BaseModel):
    product_id: int
    name: str
    quantity: int
    unit_price: float


class OrderOut(BaseModel):
    order_id: int
    session_id: str
    shipping_address: str
    status: str
    total_amount: float
    created_at: datetime
    items: list[OrderItemOut]


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=120)
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    session_id: str
    reply: str


class OrderHistoryOut(BaseModel):
    orders: list[OrderOut]
