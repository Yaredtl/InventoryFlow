from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.transaction import TransactionType


# --- Escritura ---

class TransactionCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    type: TransactionType
    force: bool = Field(
        default=False,
        description="Si es True y no hay stock suficiente, despacha lo disponible en lugar de rechazar.",
    )


# --- Lectura ---

class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    type: TransactionType
    created_at: datetime
    # Presente solo cuando se realizó un despacho parcial (force=True)
    warning: str | None = None
    quantity_requested: int | None = None


# --- Respuesta de conflicto de stock (HTTP 409) ---

class StockConflict(BaseModel):
    """Devuelto cuando hay stock insuficiente y force=False.
    El frontend debe mostrar confirmación al usuario."""

    detail: str
    product_id: int
    quantity_requested: int
    available_stock: int
    requires_confirmation: bool = True
