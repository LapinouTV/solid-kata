import math
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    quantity: int

    def restock(self, amount: int) -> None:
        self.quantity += amount


@dataclass
class DigitalProduct(Product):
    # ✅ still honors the Product contract: quantity stays a comparable number
    quantity: float = math.inf

    def restock(self, amount: int) -> None:
        print("Digital products are unlimited, nothing to restock")


@dataclass
class Catalog:
    products: list[Product]

    def notify_low_stock(self, threshold: int = 5) -> None:
        for product in self.products:
            # ✅ works everywhere a Product works, no special-casing needed
            if product.quantity < threshold:
                print(f"⚠️  Low stock alert: {product.name}")


def main() -> None:
    catalog = Catalog(
        products=[
            Product("Keyboard", 49.99, 3),
            DigitalProduct("E-book", 9.99),
        ]
    )
    catalog.notify_low_stock()


if __name__ == "__main__":
    main()
