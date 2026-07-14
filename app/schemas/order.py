from datetime import datetime

from pydantic import BaseModel, Field


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


class OrderHistoryOut(BaseModel):
    orders: list[OrderOut]
