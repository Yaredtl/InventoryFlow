from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


def _get_category_or_404(category_id: int, db: Session) -> Category:
    """Obtiene una categoría por ID o lanza 404 con mensaje en español."""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ninguna categoría con el ID {category_id}.",
        )
    return category


def _check_nombre_duplicado(name: str, db: Session, exclude_id: int | None = None) -> None:
    """Lanza 409 si ya existe otra categoría con el mismo nombre."""
    query = db.query(Category).filter(Category.name == name)
    if exclude_id is not None:
        query = query.filter(Category.id != exclude_id)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría con el nombre '{name}'.",
        )


@router.get("/", response_model=list[CategoryRead])
def listar_categorias(db: Session = Depends(get_db)) -> list[Category]:
    return db.query(Category).order_by(Category.name).all()


@router.get("/{category_id}", response_model=CategoryRead)
def obtener_categoria(category_id: int, db: Session = Depends(get_db)) -> Category:
    return _get_category_or_404(category_id, db)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def crear_categoria(payload: CategoryCreate, db: Session = Depends(get_db)) -> Category:
    _check_nombre_duplicado(payload.name, db)

    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.patch("/{category_id}", response_model=CategoryRead)
def actualizar_categoria(
    category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)
) -> Category:
    category = _get_category_or_404(category_id, db)

    cambios = payload.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar.",
        )

    if "name" in cambios:
        _check_nombre_duplicado(cambios["name"], db, exclude_id=category_id)

    for field, value in cambios.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def eliminar_categoria(category_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    category = _get_category_or_404(category_id, db)

    productos_afectados = len(category.products)
    db.delete(category)
    db.commit()

    if productos_afectados > 0:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "mensaje": (
                    f"Categoría '{category.name}' eliminada correctamente. "
                    f"{productos_afectados} producto(s) han quedado sin categoría asignada."
                ),
                "productos_desvinculados": productos_afectados,
            },
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"mensaje": f"Categoría '{category.name}' eliminada correctamente."},
    )
