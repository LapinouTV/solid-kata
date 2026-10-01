from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float
    quantity: int
    category: str


@dataclass
class Catalog:
    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def total_price(self) -> float:
        total = 0.0
        for product in self.products:
            subtotal = product.price * product.quantity
            if product.category == "electronics":
                subtotal *= 0.90  # 10% off electronics
            elif product.category == "food":
                subtotal *= 0.95  # 5% off food
            elif product.category == "clothing":
                subtotal *= 0.80  # 20% off clothing
            # Tomorrow: a "books" category? We'll have to edit this again.
            total += subtotal
        return total


def main() -> None:
    catalog = Catalog()
    catalog.add_product(Product("Laptop", 1000.0, 1, "electronics"))
    catalog.add_product(Product("Apple", 2.0, 10, "food"))
    catalog.add_product(Product("Shirt", 25.0, 3, "clothing"))

    print(f"Total: ${catalog.total_price():.2f}")


if __name__ == "__main__":
    main()
