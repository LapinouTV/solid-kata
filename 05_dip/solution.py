from dataclasses import dataclass, field
from typing import Protocol


class Database:
    def save(self, table: str, value: str) -> None:
        print(f"Saving '{value}' into '{table}' table")


@dataclass
class Product:
    name: str
    price: float
    quantity: int


class ProductRepository(Protocol):
    def save_products(self, products: list[Product]) -> None: ...


class DatabaseProductRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def save_products(self, products: list[Product]) -> None:
        for product in products:
            self._database.save("product", product.name)


class InMemoryProductRepository:
    # ✅ Easy to swap in for tests, no database needed
    def __init__(self) -> None:
        self.saved: list[str] = []

    def save_products(self, products: list[Product]) -> None:
        self.saved.extend(product.name for product in products)


@dataclass
class Catalog:
    repository: ProductRepository
    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def save(self) -> None:
        self.repository.save_products(self.products)


def main() -> None:
    catalog = Catalog(repository=DatabaseProductRepository(Database()))
    catalog.add_product(Product("Keyboard", 49.99, 10))
    catalog.save()


if __name__ == "__main__":
    main()
