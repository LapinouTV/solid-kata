from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class Product:
    name: str
    price: float
    quantity: int
    category: str


class DiscountStrategy(Protocol):
    def supports(self, category: str) -> bool: ...
    def apply(self, subtotal: float) -> float: ...


class ElectronicsDiscount:
    def supports(self, category: str) -> bool:
        return category == "electronics"

    def apply(self, subtotal: float) -> float:
        return subtotal * 0.90


class FoodDiscount:
    def supports(self, category: str) -> bool:
        return category == "food"

    def apply(self, subtotal: float) -> float:
        return subtotal * 0.95


class ClothingDiscount:
    def supports(self, category: str) -> bool:
        return category == "clothing"

    def apply(self, subtotal: float) -> float:
        return subtotal * 0.80


# ✅ Adding "books" only requires a new class, no existing code changes
class BooksDiscount:
    def supports(self, category: str) -> bool:
        return category == "books"

    def apply(self, subtotal: float) -> float:
        return subtotal * 0.85


@dataclass
class Catalog:
    discount_strategies: list[DiscountStrategy]
    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def total_price(self) -> float:
        total = 0.0
        for product in self.products:
            subtotal = product.price * product.quantity
            for strategy in self.discount_strategies:
                if strategy.supports(product.category):
                    subtotal = strategy.apply(subtotal)
                    break
            total += subtotal
        return total


def main() -> None:
    catalog = Catalog(
        discount_strategies=[
            ElectronicsDiscount(),
            FoodDiscount(),
            ClothingDiscount(),
            BooksDiscount(),
        ]
    )
    catalog.add_product(Product("Laptop", 1000.0, 1, "electronics"))
    catalog.add_product(Product("Apple", 2.0, 10, "food"))
    catalog.add_product(Product("Shirt", 25.0, 3, "clothing"))
    catalog.add_product(Product("Novel", 15.0, 2, "books"))

    print(f"Total: ${catalog.total_price():.2f}")


if __name__ == "__main__":
    main()
