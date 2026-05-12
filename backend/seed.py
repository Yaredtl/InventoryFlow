"""
Seeder para InventoryFlow.
Crea 4 categorias, 2 productos por categoria y 4 transacciones de ejemplo.

Uso:
    cd backend
    .\.venv\Scripts\python.exe seed.py

El script es idempotente: si los datos ya existen (mismo SKU o nombre de
categoria) los omite sin lanzar error.
"""

import sys
from decimal import Decimal

from app.db.session import SessionLocal
from app.models.category import Category
from app.models.product import Product
from app.models.transaction import Transaction, TransactionType

# ──────────────────────────────────────────────────────────────
# Datos de ejemplo
# ──────────────────────────────────────────────────────────────

CATEGORIES = [
    {"name": "Bebidas",    "description": "Refrescos, aguas, zumos y bebidas energeticas"},
    {"name": "Lacteos",    "description": "Leche, yogures, quesos y mantequilla"},
    {"name": "Snacks",     "description": "Patatas fritas, frutos secos y galletas"},
    {"name": "Limpieza",   "description": "Productos de limpieza del hogar"},
]

PRODUCTS = [
    # Bebidas
    {"name": "Agua Mineral 1.5L",   "sku": "BEB-AGU-001", "price": Decimal("0.59"),  "current_stock": 200, "min_stock_threshold": 40,  "category": "Bebidas"},
    {"name": "Refresco Cola 33cl",   "sku": "BEB-COL-001", "price": Decimal("0.99"),  "current_stock": 150, "min_stock_threshold": 30,  "category": "Bebidas"},
    # Lacteos
    {"name": "Leche Entera 1L",      "sku": "LAC-LEC-001", "price": Decimal("1.05"),  "current_stock": 80,  "min_stock_threshold": 20,  "category": "Lacteos"},
    {"name": "Yogur Natural 4ud",    "sku": "LAC-YOG-001", "price": Decimal("1.29"),  "current_stock": 60,  "min_stock_threshold": 15,  "category": "Lacteos"},
    # Snacks
    {"name": "Patatas Fritas 150g",  "sku": "SNK-PAT-001", "price": Decimal("1.49"),  "current_stock": 10,  "min_stock_threshold": 20,  "category": "Snacks"},
    {"name": "Frutos Secos Mix 200g","sku": "SNK-FRU-001", "price": Decimal("2.99"),  "current_stock": 45,  "min_stock_threshold": 10,  "category": "Snacks"},
    # Limpieza
    {"name": "Detergente Liquido 2L","sku": "LIM-DET-001", "price": Decimal("4.95"),  "current_stock": 0,   "min_stock_threshold": 10,  "category": "Limpieza"},
    {"name": "Lejia 1.5L",           "sku": "LIM-LEJ-001", "price": Decimal("1.20"),  "current_stock": 35,  "min_stock_threshold": 10,  "category": "Limpieza"},
]

# Las transacciones referencian productos por SKU
TRANSACTIONS = [
    {"sku": "BEB-AGU-001", "quantity": 100, "type": TransactionType.IN},
    {"sku": "LAC-LEC-001", "quantity": 25,  "type": TransactionType.OUT},
    {"sku": "SNK-PAT-001", "quantity": 50,  "type": TransactionType.IN},
    {"sku": "LIM-DET-001", "quantity": 30,  "type": TransactionType.IN},
]


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def _upsert_category(db, data: dict) -> Category:
    obj = db.query(Category).filter_by(name=data["name"]).first()
    if obj:
        print(f"  [SKIP] Categoria ya existe: {data['name']}")
        return obj
    obj = Category(**data)
    db.add(obj)
    db.flush()
    print(f"  [OK]   Categoria creada:       {data['name']}")
    return obj


def _upsert_product(db, data: dict, category_map: dict) -> Product:
    obj = db.query(Product).filter_by(sku=data["sku"]).first()
    if obj:
        print(f"  [SKIP] Producto ya existe:  {data['sku']}")
        return obj
    payload = {k: v for k, v in data.items() if k != "category"}
    payload["category_id"] = category_map[data["category"]]
    obj = Product(**payload)
    db.add(obj)
    db.flush()
    print(f"  [OK]   Producto creado:        {data['sku']} - {data['name']}")
    return obj


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

def run():
    db = SessionLocal()
    try:
        print("\n=== Seeder InventoryFlow ===\n")

        # Categorias
        print(">> Categorias")
        category_map: dict[str, int] = {}
        for cat_data in CATEGORIES:
            cat = _upsert_category(db, cat_data)
            category_map[cat.name] = cat.id

        # Productos
        print("\n>> Productos")
        product_map: dict[str, int] = {}
        for prod_data in PRODUCTS:
            prod = _upsert_product(db, prod_data, category_map)
            product_map[prod_data["sku"]] = prod.id

        # Transacciones (siempre se insertan — son registros historicos)
        print("\n>> Transacciones")
        for tx_data in TRANSACTIONS:
            sku = tx_data["sku"]
            product_id = product_map.get(sku)
            if not product_id:
                print(f"  [WARN] Producto no encontrado para SKU {sku}, omitiendo transaccion.")
                continue
            tx = Transaction(
                product_id=product_id,
                quantity=tx_data["quantity"],
                type=tx_data["type"],
            )
            db.add(tx)
            print(f"  [OK]   Transaccion: {tx_data['type'].value} {tx_data['quantity']}u  -> {sku}")

        db.commit()
        print("\n✓ Seeder completado correctamente.\n")

    except Exception as exc:
        db.rollback()
        print(f"\n✗ Error durante el seed: {exc}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    run()
