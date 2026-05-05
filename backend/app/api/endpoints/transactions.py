from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.product import Product
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import StockConflict, TransactionCreate, TransactionRead

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/", response_model=list[TransactionRead])
def list_transactions(db: Session = Depends(get_db)) -> list[Transaction]:
    return db.query(Transaction).order_by(Transaction.created_at.desc()).all()


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)) -> Transaction:
    tx = db.get(Transaction, transaction_id)
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return tx


@router.post(
    "/",
    response_model=TransactionRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {
            "model": StockConflict,
            "description": "Stock insuficiente. El cliente puede reenviar con force=true para despachar lo disponible.",
        }
    },
)
def create_transaction(
    payload: TransactionCreate, db: Session = Depends(get_db)
) -> Transaction | JSONResponse:
    product = db.get(Product, payload.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    warning: str | None = None
    quantity_to_dispatch = payload.quantity

    if payload.type == TransactionType.OUT:
        if payload.quantity > product.current_stock:
            if not payload.force:
                # --- Paso 1: informar al FE del conflicto, sin hacer nada ---
                conflict = StockConflict(
                    detail=(
                        f"Stock insuficiente. Se solicitaron {payload.quantity} unidades "
                        f"pero solo hay {product.current_stock} disponibles."
                    ),
                    product_id=payload.product_id,
                    quantity_requested=payload.quantity,
                    available_stock=product.current_stock,
                )
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content=conflict.model_dump(),
                )

            # --- Paso 2: force=True → despachar lo que hay ---
            quantity_to_dispatch = product.current_stock
            warning = (
                f"Despacho parcial: se solicitaron {payload.quantity} unidades "
                f"pero solo se despacharon {quantity_to_dispatch}. Stock agotado."
            )

        product.current_stock -= quantity_to_dispatch
    else:
        # Tipo IN: siempre suma el total solicitado
        product.current_stock += quantity_to_dispatch

    tx = Transaction(
        product_id=payload.product_id,
        quantity=quantity_to_dispatch,
        type=payload.type,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    # Adjuntamos los campos extra al objeto para que Pydantic los serialice
    tx.warning = warning  # type: ignore[attr-defined]
    tx.quantity_requested = payload.quantity if warning else None  # type: ignore[attr-defined]
    return tx
