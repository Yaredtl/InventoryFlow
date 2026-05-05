from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router

app = FastAPI(
    title="InventoryFlow API",
    version="1.0.0",
    description="Sistema de gestión de inventario para Dark Stores",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def handler_errores_validacion(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Convierte los errores 422 de Pydantic a mensajes limpios en español."""
    errores = []
    for error in exc.errors():
        # loc = ("body", "campo") → nos quedamos solo con el nombre del campo
        campo = error["loc"][-1] if len(error["loc"]) > 1 else str(error["loc"][0])
        # Pydantic añade "Value error, " al inicio del msg cuando usamos field_validator
        mensaje = error["msg"].removeprefix("Value error, ")
        errores.append({"campo": str(campo), "mensaje": mensaje})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Los datos enviados no son válidos.",
            "detalle": errores,
        },
    )


app.include_router(api_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
