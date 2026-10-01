from dataclasses import dataclass, field


class Database:
    def save(self, table: str, value: str) -> None:
        print(f"Saving '{value}' into '{table}' table")


@dataclass
class Product:
    name: str
    price: float
    quantity: int


@dataclass
class Catalog:
    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def save(self) -> None:
        # ❌ High-level Catalog constructs and depends on a concrete Database
        database = Database()
        for product in self.products:
            database.save("product", product.name)


def main() -> None:
    catalog = Catalog()
    catalog.add_product(Product("Keyboard", 49.99, 10))
    # can't swap Database for a fake/test double without editing Catalog
    catalog.save()


if __name__ == "__main__":
    main()
