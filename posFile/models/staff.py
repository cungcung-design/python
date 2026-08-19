from dataclasses import dataclass
from typing import Optional


@dataclass
class Staff:
    id: Optional[int]
    name: str
    role: str
