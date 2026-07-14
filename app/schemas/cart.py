from pydantic import BaseModel, Field


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
