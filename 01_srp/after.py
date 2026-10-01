from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float
    quantity: int


@dataclass
class Catalog:
    """Represents a product catalog"""

    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)


class ReceiptPrinter:
    """Dedicated class that formats and prints a receipt for a catalog"""

    def print(self, catalog: Catalog) -> None:
        total = 0.0
        print("=== Receipt ===")
        for product in catalog.products:
            subtotal = product.price * product.quantity
            total += subtotal
            print(f"{product.name} x{product.quantity} - ${subtotal:.2f}")
        print(f"Total: ${total:.2f}")


class CatalogRepository:
    """Dedicated class that persists a catalog's products"""

    def __init__(self, db: "Database"):
        self._db = db

    def save(self, catalog: Catalog) -> None:
        for product in catalog.products:
            self._db.save("product", product.name)


class StockAlertNotifier:
    """Dedicated class that warns about low stock"""

    def notify(self, catalog: Catalog, threshold: int = 5) -> None:
        for product in catalog.products:
            if product.quantity < threshold:
                print(
                    f"⚠️  Low stock alert: {product.name} has only {product.quantity} left"
                )


class Database:
    def save(self, table: str, value: str) -> None:
        print(f"Saving '{value}' into '{table}' table")


def main() -> None:
    catalog = Catalog()
    catalog.add_product(Product(name="Keyboard", price=49.99, quantity=10))
    catalog.add_product(Product(name="Mouse", price=19.99, quantity=3))

    ReceiptPrinter().print(catalog)
    CatalogRepository(Database()).save(catalog)
    StockAlertNotifier().notify(catalog)


if __name__ == "__main__":
    main()
