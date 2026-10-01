from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class Product:
    name: str
    price: float
    quantity: int


class ProductExporter(Protocol):
    def export_to_csv(self, products: list[Product]) -> str: ...
    def export_to_pdf(self, products: list[Product]) -> bytes: ...


class CsvProductExporter:
    def export_to_csv(self, products: list[Product]) -> str:
        lines = [f"{p.name},{p.price},{p.quantity}" for p in products]
        return "\n".join(lines)

    # ❌ This exporter only knows CSV, but the interface also requires PDF
    def export_to_pdf(self, products: list[Product]) -> bytes:
        raise NotImplementedError("CSV exporter can't produce PDF")


@dataclass
class Catalog:
    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)


def main() -> None:
    catalog = Catalog()
    catalog.add_product(Product("Keyboard", 49.99, 10))

    exporter: ProductExporter = CsvProductExporter()
    print(exporter.export_to_csv(catalog.products))
    exporter.export_to_pdf(catalog.products)  # 💥 blows up at runtime


if __name__ == "__main__":
    main()
