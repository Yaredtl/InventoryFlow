from pydantic import BaseModel, ConfigDict, Field, field_validator


# --- Escritura ---

class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float = Field(gt=0, description="El precio debe ser mayor que cero.")
    current_stock: int = Field(default=0, ge=0, description="El stock no puede ser negativo.")
    min_stock_threshold: int = Field(default=0, ge=0, description="El umbral mínimo no puede ser negativo.")
    category_id: int | None = None

    @field_validator("name")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El nombre del producto no puede estar vacío.")
        if len(v) > 150:
            raise ValueError("El nombre no puede superar los 150 caracteres.")
        return v

    @field_validator("sku")
    @classmethod
    def validar_sku(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("El SKU no puede estar vacío.")
        if len(v) > 50:
            raise ValueError("El SKU no puede superar los 50 caracteres.")
        if " " in v:
            raise ValueError("El SKU no puede contener espacios.")
        return v


class ProductUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    price: float | None = Field(default=None, gt=0, description="El precio debe ser mayor que cero.")
    current_stock: int | None = Field(default=None, ge=0, description="El stock no puede ser negativo.")
    min_stock_threshold: int | None = Field(default=None, ge=0, description="El umbral mínimo no puede ser negativo.")
    category_id: int | None = None

    @field_validator("name")
    @classmethod
    def validar_nombre(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("El nombre del producto no puede estar vacío.")
            if len(v) > 150:
                raise ValueError("El nombre no puede superar los 150 caracteres.")
        return v

    @field_validator("sku")
    @classmethod
    def validar_sku(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip().upper()
            if not v:
                raise ValueError("El SKU no puede estar vacío.")
            if len(v) > 50:
                raise ValueError("El SKU no puede superar los 50 caracteres.")
            if " " in v:
                raise ValueError("El SKU no puede contener espacios.")
        return v


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
