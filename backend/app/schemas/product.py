from pydantic import BaseModel, ConfigDict, Field


# --- Escritura ---

class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float = Field(gt=0)
    current_stock: int = Field(default=0, ge=0)
    min_stock_threshold: int = Field(default=0, ge=0)
    category_id: int | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    price: float | None = Field(default=None, gt=0)
    current_stock: int | None = Field(default=None, ge=0)
    min_stock_threshold: int | None = Field(default=None, ge=0)
    category_id: int | None = None


# --- Lectura ---

class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sku: str
    price: float
    current_stock: int
    min_stock_threshold: int
    category_id: int | None

    @property
    def is_low_stock(self) -> bool:
        return self.current_stock <= self.min_stock_threshold
