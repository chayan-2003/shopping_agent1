from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.db.models import Product


def search_products(
    db: Session,
    query: str | None = None,
    category: str | None = None,
    max_price: float | None = None,
    limit: int = 20,
) -> list[Product]:
    filters = []
    if query:
        like = f"%{query.strip()}%"
        filters.append((Product.name.ilike(like)) | (Product.description.ilike(like)))
    if category:
        filters.append(Product.category.ilike(category.strip()))
    if max_price is not None:
        filters.append(Product.price <= max_price)

    stmt = select(Product)
    if filters:
        stmt = stmt.where(and_(*filters))

    stmt = stmt.order_by(Product.price.asc()).limit(limit)
    return list(db.scalars(stmt))


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)
