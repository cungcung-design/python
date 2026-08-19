from database.database import Database
from models.category import Category
from models.product import Product


class ProductService:
    def __init__(self, db: Database, audit_service=None):
        self.db = db
        self.audit_service = audit_service

    def get_all_products(self) -> list:
        return self.db.fetch_all("SELECT id, name, price, barcode, category_id, stock_quantity FROM items")

    def get_product_by_id(self, product_id: int) -> Product | None:
        row = self.db.fetch_all("SELECT id, name, price, barcode, category_id, stock_quantity FROM items WHERE id = %s", (product_id,))
        if row:
            r = row[0]
            return Product(id=r[0], name=r[1], price=float(r[2]), barcode=r[3], category_id=r[4], stock_quantity=r[5])
        return None

    def get_product_by_barcode(self, barcode: str) -> Product | None:
        row = self.db.fetch_all("SELECT id, name, price, barcode, category_id, stock_quantity FROM items WHERE barcode = %s", (barcode,))
        if row:
            r = row[0]
            return Product(id=r[0], name=r[1], price=float(r[2]), barcode=r[3], category_id=r[4], stock_quantity=r[5])
        return None

    def create_product(self, product: Product, user_id=None):
        self.db.execute_query(
            "INSERT INTO items (name, price, barcode, category_id, stock_quantity) VALUES (%s, %s, %s, %s, %s)",
            (product.name, product.price, product.barcode, product.category_id, product.stock_quantity),
        )
        if self.audit_service and user_id:
            self.audit_service.log(
                user_id,
                "PRODUCT_CREATED",
                "Product",
                product.id,
                f"Created product: {product.name}",
            )

    def update_product(self, product: Product, user_id=None, old_product=None):
        if old_product and self.audit_service and user_id:
            changes = []
            if old_product.name != product.name:
                changes.append(f"Name changed from {old_product.name} to {product.name}")
            if float(old_product.price) != float(product.price):
                changes.append(f"Price changed from RM{float(old_product.price):.2f} to RM{float(product.price):.2f}")
            if int(old_product.stock_quantity) != int(product.stock_quantity):
                changes.append(f"Stock changed from {old_product.stock_quantity} to {product.stock_quantity}")

            if changes:
                self.audit_service.log(
                    user_id,
                    "PRODUCT_UPDATED",
                    "Product",
                    product.id,
                    "; ".join(changes),
                )

        self.db.execute_query(
            "UPDATE items SET name=%s, price=%s, barcode=%s, category_id=%s, stock_quantity=%s WHERE id=%s",
            (product.name, product.price, product.barcode, product.category_id, product.stock_quantity, product.id),
        )

    def delete_product(self, product_id: int, user_id=None):
        if self.audit_service and user_id:
            self.audit_service.log(
                user_id,
                "PRODUCT_DEACTIVATED",
                "Product",
                product_id,
                f"Product ID {product_id} deactivated",
            )
        self.db.execute_query("DELETE FROM items WHERE id = %s", (product_id,))
