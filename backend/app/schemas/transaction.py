from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.transaction import TransactionType


# --- Escritura ---

class TransactionCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    type: TransactionType


# --- Lectura ---

class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    type: TransactionType
    created_at: datetime
