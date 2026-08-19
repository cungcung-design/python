from unittest.mock import MagicMock

from services.product_service import ProductService
from models.product import Product


class FakeProductDatabase:
    def __init__(self):
        self.products = {
            1: (1, "Coffee", 5.50, "123456", 1, 20),
            2: (2, "Bread", 3.00, "654321", 1, 5),
        }
        self.next_id = 3

    def fetch_all(self, query, params=None):
        normalized = " ".join(query.lower().split())
        if "from items" in normalized:
            if "where id" in normalized:
                product_id = params[0]
                if product_id in self.products:
                    return [self.products[product_id]]
                return []
            if "where barcode" in normalized:
                barcode = params[0]
                for p in self.products.values():
                    if p[3] == barcode:
                        return [p]
                return []
            return list(self.products.values())
        return []

    def execute_query(self, query, params=None):
        query_lower = query.lower()
        if "insert into items" in query_lower:
            product_id = self.next_id
            self.products[product_id] = (
                product_id,
                params[0],
                params[1],
                params[2],
                params[3],
                params[4],
            )
            self.next_id += 1
        elif "update items" in query_lower:
            product_id = params[5]
            self.products[product_id] = (
                product_id,
                params[0],
                params[1],
                params[2],
                params[3],
                params[4],
            )
        elif "delete from items" in query_lower:
            product_id = params[0]
            self.products.pop(product_id, None)
        return MagicMock()


def test_get_all_products():
    db = FakeProductDatabase()
    service = ProductService(db)
    products = service.get_all_products()
    assert len(products) == 2


def test_get_product_by_id():
    db = FakeProductDatabase()
    service = ProductService(db)
    product = service.get_product_by_id(1)
    assert product is not None
    assert product.name == "Coffee"
    assert product.price == 5.50


def test_get_product_by_barcode():
    db = FakeProductDatabase()
    service = ProductService(db)
    product = service.get_product_by_barcode("123456")
    assert product is not None
    assert product.id == 1


def test_create_product():
    db = FakeProductDatabase()
    service = ProductService(db)
    new_product = Product(
        id=None,
        name="Tea",
        price=4.00,
        barcode="999999",
        category_id=1,
        stock_quantity=15,
    )
    service.create_product(new_product)
    products = service.get_all_products()
    assert len(products) == 3


def test_update_product():
    db = FakeProductDatabase()
    service = ProductService(db)
    product = service.get_product_by_id(1)
    product.name = "Iced Coffee"
    product.price = 6.00
    service.update_product(product)
    updated = service.get_product_by_id(1)
    assert updated.name == "Iced Coffee"
    assert updated.price == 6.00


def test_delete_product():
    db = FakeProductDatabase()
    service = ProductService(db)
    service.delete_product(1)
    products = service.get_all_products()
    assert len(products) == 1
    assert service.get_product_by_id(1) is None