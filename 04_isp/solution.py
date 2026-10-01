from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class Product:
    name: str
    price: float
    quantity: int


class CsvExporter(Protocol):
    def export_to_csv(self, products: list[Product]) -> str: ...


class PdfExporter(Protocol):
    def export_to_pdf(self, products: list[Product]) -> bytes: ...


class CsvProductExporter(CsvExporter):
    def export_to_csv(self, products: list[Product]) -> str:
        lines = [f"{p.name},{p.price},{p.quantity}" for p in products]
        return "\n".join(lines)


class PdfProductExporter(PdfExporter):
    def export_to_pdf(self, products: list[Product]) -> bytes:
        return f"PDF report for {len(products)} product(s)".encode()


@dataclass
class Catalog:
    products: list[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)


class CatalogExportService:
    # ✅ Depends only on the interface it actually needs
    def __init__(self, csv_exporter: CsvExporter) -> None:
        self._csv_exporter = csv_exporter

    def export(self, catalog: Catalog) -> str:
        return self._csv_exporter.export_to_csv(catalog.products)


def main() -> None:
    catalog = Catalog()
    catalog.add_product(Product("Keyboard", 49.99, 10))

    service = CatalogExportService(CsvProductExporter())
    print(service.export(catalog))


if __name__ == "__main__":
    main()
