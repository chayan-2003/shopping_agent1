import json

from langchain.tools import tool
from sqlalchemy.orm import Session

from app.services.cart_service import add_item_to_cart, get_cart_summary, remove_item_from_cart
from app.services.catalog_service import search_products
from app.services.order_service import checkout, get_order_history


def build_tools(db: Session, session_id: str):
    @tool
    def search_catalog(query: str = "", category: str = "", max_price: float | None = None) -> str:
        """Search products by query, category, and max price and return product details with IDs."""
        products = search_products(
            db,
            query=query or None,
            category=category or None,
            max_price=max_price,
            limit=10,
        )
        data = [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": round(p.price, 2),
                "stock": p.stock,
                "description": p.description,
            }
            for p in products
        ]
        return json.dumps(data)

    @tool
    def add_to_cart(product_id: int, quantity: int = 1) -> str:
        """Add a quantity of a product into the current user's cart by product_id."""
        summary = add_item_to_cart(db, session_id=session_id, product_id=product_id, quantity=quantity)
        return json.dumps(summary)

    @tool
    def remove_from_cart(product_id: int) -> str:
        """Remove a product from the current user's cart by product_id."""
        summary = remove_item_from_cart(db, session_id=session_id, product_id=product_id)
        return json.dumps(summary)

    @tool
    def view_cart() -> str:
        """View the current user's cart summary and totals."""
        summary = get_cart_summary(db, session_id=session_id)
        return json.dumps(summary)

    @tool
    def place_order(shipping_address: str) -> str:
        """Checkout current cart and place an order to a shipping address."""
        result = checkout(db, session_id=session_id, shipping_address=shipping_address)
        return json.dumps(result, default=str)

    @tool
    def view_order_history() -> str:
        """View all past orders for the current user."""
        orders = get_order_history(db, session_id=session_id)
        return json.dumps(orders, default=str)

    return [search_catalog, add_to_cart, remove_from_cart, view_cart, place_order, view_order_history]
