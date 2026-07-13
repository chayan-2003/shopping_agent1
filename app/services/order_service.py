from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CartItem, Order, OrderItem
from app.services.cart_service import clear_cart, get_cart_summary
from app.services.catalog_service import get_product_by_id


def checkout(db: Session, session_id: str, shipping_address: str) -> dict:
    cart_items = db.scalars(select(CartItem).where(CartItem.session_id == session_id)).all()
    if not cart_items:
        raise ValueError("Cart is empty")

    cart_summary = get_cart_summary(db, session_id)
    if not cart_summary["items"]:
        raise ValueError("Cart has no valid items")

    order = Order(
        session_id=session_id,
        shipping_address=shipping_address,
        total_amount=cart_summary["subtotal"],
        status="created",
    )
    db.add(order)
    db.flush()

    order_items: list[dict] = []
    for cart_item in cart_items:
        product = get_product_by_id(db, cart_item.product_id)
        if not product:
            continue
        if cart_item.quantity > product.stock:
            raise ValueError(f"Insufficient stock for {product.name}")
        product.stock -= cart_item.quantity

        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=cart_item.quantity,
                unit_price=product.price,
            )
        )
        order_items.append(
            {
                "product_id": product.id,
                "name": product.name,
                "quantity": cart_item.quantity,
                "unit_price": round(product.price, 2),
            }
        )

    db.commit()
    clear_cart(db, session_id)

    return {
        "order_id": order.id,
        "session_id": session_id,
        "shipping_address": order.shipping_address,
        "status": order.status,
        "total_amount": round(order.total_amount, 2),
        "created_at": order.created_at,
        "items": order_items,
    }


def get_order_history(db: Session, session_id: str) -> list[dict]:
    """Retrieve all orders for a given session_id."""
    orders = db.scalars(
        select(Order).where(Order.session_id == session_id).order_by(Order.created_at.desc())
    ).all()

    result = []
    for order in orders:
        order_items = [
            {
                "product_id": item.product_id,
                "name": item.product.name,
                "quantity": item.quantity,
                "unit_price": round(item.unit_price, 2),
            }
            for item in order.items
        ]
        result.append(
            {
                "order_id": order.id,
                "session_id": order.session_id,
                "shipping_address": order.shipping_address,
                "status": order.status,
                "total_amount": round(order.total_amount, 2),
                "created_at": order.created_at,
                "items": order_items,
            }
        )
    return result
