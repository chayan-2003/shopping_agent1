from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import CartItem
from app.services.catalog_service import get_product_by_id


def add_item_to_cart(db: Session, session_id: str, product_id: int, quantity: int) -> dict:
    product = get_product_by_id(db, product_id)
    if not product:
        raise ValueError("Product not found")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    existing = db.scalar(
        select(CartItem).where(CartItem.session_id == session_id, CartItem.product_id == product_id)
    )
    new_quantity = quantity
    if existing:
        new_quantity = existing.quantity + quantity
    if new_quantity > product.stock:
        raise ValueError(f"Only {product.stock} items are in stock for {product.name}")

    if existing:
        existing.quantity = new_quantity
    else:
        db.add(CartItem(session_id=session_id, product_id=product_id, quantity=quantity))
    db.commit()

    return get_cart_summary(db, session_id)


def remove_item_from_cart(db: Session, session_id: str, product_id: int) -> dict:
    item = db.scalar(
        select(CartItem).where(CartItem.session_id == session_id, CartItem.product_id == product_id)
    )
    if item:
        db.delete(item)
        db.commit()
    return get_cart_summary(db, session_id)


def clear_cart(db: Session, session_id: str) -> None:
    items = db.scalars(select(CartItem).where(CartItem.session_id == session_id)).all()
    for item in items:
        db.delete(item)
    db.commit()


def get_cart_summary(db: Session, session_id: str) -> dict:
    items = db.scalars(select(CartItem).where(CartItem.session_id == session_id)).all()
    rows: list[dict] = []
    total_items = 0
    subtotal = 0.0

    for item in items:
        product = get_product_by_id(db, item.product_id)
        if not product:
            continue
        line_total = round(product.price * item.quantity, 2)
        rows.append(
            {
                "product_id": product.id,
                "name": product.name,
                "quantity": item.quantity,
                "unit_price": round(product.price, 2),
                "line_total": line_total,
            }
        )
        total_items += item.quantity
        subtotal += line_total

    return {
        "session_id": session_id,
        "items": rows,
        "total_items": total_items,
        "subtotal": round(subtotal, 2),
    }
