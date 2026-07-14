from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import ProductOut
from app.services.catalog_service import search_products

router = APIRouter(tags=["products"])


@router.get("/products", response_model=list[ProductOut])
def list_products(
    query: str | None = None,
    category: str | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db),
) -> list[ProductOut]:
    products = search_products(db, query=query, category=category, max_price=max_price)
    return [ProductOut.model_validate(p) for p in products]
