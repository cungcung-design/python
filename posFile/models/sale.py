from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Sale:
    id: Optional[int]
    item_id: int
    quantity: int
    total: float
    date: datetime
    staff_id: int
