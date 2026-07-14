from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Product


DEFAULT_PRODUCTS = [
    {
        "name": "Wireless Earbuds A1",
        "description": "Bluetooth 5.3 earbuds with noise reduction and 24h battery life.",
        "category": "Audio",
        "price": 39.99,
        "stock": 120,
    },
    {
        "name": "Over-Ear Headphones Pro",
        "description": "Over-ear ANC headphones with rich bass and USB-C fast charging.",
        "category": "Audio",
        "price": 129.00,
        "stock": 55,
    },
    {
        "name": "Smartwatch Fit 2",
        "description": "Fitness smartwatch with heart-rate tracking and GPS.",
        "category": "Wearables",
        "price": 89.50,
        "stock": 73,
    },
    {
        "name": "USB-C Charger 65W",
        "description": "Compact GaN charger with dual USB-C ports.",
        "category": "Accessories",
        "price": 29.99,
        "stock": 200,
    },
    {
        "name": "Gaming Mouse G7",
        "description": "Lightweight RGB gaming mouse with 16000 DPI sensor.",
        "category": "Computer",
        "price": 49.99,
        "stock": 95,
    },
    {
        "name": "Mechanical Keyboard K80",
        "description": "Hot-swappable mechanical keyboard with tactile switches.",
        "category": "Computer",
        "price": 99.99,
        "stock": 64,
    },
]


def seed_products_if_empty(db: Session) -> None:
    product_exists = db.scalar(select(Product.id).limit(1))
    if product_exists:
        return

    for product in DEFAULT_PRODUCTS:
        db.add(Product(**product))
    db.commit()
