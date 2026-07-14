from pydantic import BaseModel


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    category: str
    price: float
    stock: int

    model_config = {"from_attributes": True}
