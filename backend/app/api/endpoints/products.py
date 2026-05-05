from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


def _get_product_or_404(product_id: int, db: Session) -> Product:
    """Obtiene un producto por ID o lanza 404 con mensaje en español."""
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún producto con el ID {product_id}.",
        )
    return product


def _check_sku_duplicado(sku: str, db: Session, exclude_id: int | None = None) -> None:
    """Lanza 409 si ya existe otro producto con el mismo SKU."""
    query = db.query(Product).filter(Product.sku == sku)
    if exclude_id is not None:
        query = query.filter(Product.id != exclude_id)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un producto con el SKU '{sku}'. El SKU debe ser único.",
        )


def _check_categoria_existe(category_id: int, db: Session) -> None:
    """Lanza 422 si el category_id proporcionado no existe en la base de datos."""
    if not db.get(Category, category_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"No existe ninguna categoría con el ID {category_id}. Crea la categoría primero.",
        )


@router.get("/", response_model=list[ProductRead])
def listar_productos(db: Session = Depends(get_db)) -> list[Product]:
    return db.query(Product).order_by(Product.name).all()


@router.get("/low-stock", response_model=list[ProductRead])
def listar_productos_stock_bajo(db: Session = Depends(get_db)) -> list[Product]:
    """Devuelve productos cuyo stock actual es menor o igual al umbral mínimo."""
    return (
        db.query(Product)
        .filter(Product.current_stock <= Product.min_stock_threshold)
        .order_by(Product.current_stock)
        .all()
    )


@router.get("/{product_id}", response_model=ProductRead)
def obtener_producto(product_id: int, db: Session = Depends(get_db)) -> Product:
    return _get_product_or_404(product_id, db)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def crear_producto(payload: ProductCreate, db: Session = Depends(get_db)) -> Product:
    _check_sku_duplicado(payload.sku, db)

    if payload.category_id is not None:
        _check_categoria_existe(payload.category_id, db)

    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.patch("/{product_id}", response_model=ProductRead)
def actualizar_producto(
    product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)
) -> Product:
    product = _get_product_or_404(product_id, db)

    cambios = payload.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar.",
        )

    if "sku" in cambios and cambios["sku"] is not None:
        _check_sku_duplicado(cambios["sku"], db, exclude_id=product_id)

    # Validar category_id solo si se envía un valor (None desvincula, un int debe existir)
    if "category_id" in cambios and cambios["category_id"] is not None:
        _check_categoria_existe(cambios["category_id"], db)

    for field, value in cambios.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def eliminar_producto(product_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    product = _get_product_or_404(product_id, db)

    transacciones_afectadas = len(product.transactions)
    db.delete(product)
    db.commit()

    if transacciones_afectadas > 0:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "mensaje": (
                    f"Producto '{product.name}' (SKU: {product.sku}) eliminado correctamente. "
                    f"Se han eliminado también {transacciones_afectadas} transacción(es) asociada(s)."
                ),
                "transacciones_eliminadas": transacciones_afectadas,
            },
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "mensaje": f"Producto '{product.name}' (SKU: {product.sku}) eliminado correctamente."
        },
    )
