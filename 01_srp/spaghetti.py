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

    def print_receipt(self) -> None:
        total = 0.0
        print("=== Receipt ===")
        for product in self.products:
            subtotal = product.price * product.quantity
            total += subtotal
            print(f"{product.name} x{product.quantity} - ${subtotal:.2f}")
        print(f"Total: ${total:.2f}")

    def save_to_database(self) -> None:
        database = Database()
        for product in self.products:
            database.save("product", product.name)

    def notify_low_stock(self, threshold: int = 5) -> None:
        for product in self.products:
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

    catalog.print_receipt()
    catalog.save_to_database()
    catalog.notify_low_stock()


if __name__ == "__main__":
    main()
