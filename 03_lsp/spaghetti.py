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
    # ❌ Product promises quantity is an int, but digital goods are unlimited
    quantity: int | None = None

    def restock(self, amount: int) -> None:
        # ❌ Breaks the parent's contract instead of honoring it
        print("Digital products can't be restocked, they are unlimited")


@dataclass
class Catalog:
    products: list[Product]

    def notify_low_stock(self, threshold: int = 5) -> None:
        for product in self.products:
            # 💥 Crashes with TypeError when product.quantity is None
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
