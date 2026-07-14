from app.api.routes.cart import router as cart_router
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.orders import router as orders_router
from app.api.routes.products import router as products_router

__all__ = [
    "health_router",
    "products_router",
    "cart_router",
    "orders_router",
    "chat_router",
]
