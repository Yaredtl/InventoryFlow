from pydantic import BaseModel, ConfigDict, field_validator


# --- Escritura ---

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        if len(v) > 100:
            raise ValueError("El nombre no puede superar los 100 caracteres.")
        return v

    @field_validator("description")
    @classmethod
    def validar_descripcion(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if len(v) > 500:
                raise ValueError("La descripción no puede superar los 500 caracteres.")
            return v if v else None
        return v


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validar_nombre(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("El nombre de la categoría no puede estar vacío.")
            if len(v) > 100:
                raise ValueError("El nombre no puede superar los 100 caracteres.")
        return v

    @field_validator("description")
    @classmethod
    def validar_descripcion(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if len(v) > 500:
                raise ValueError("La descripción no puede superar los 500 caracteres.")
            return v if v else None
        return v


# --- Lectura ---

class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
