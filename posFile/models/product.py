from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    id: Optional[int]
    name: str
    price: float
    barcode: str
    category_id: int
    stock_quantity: int = 0
