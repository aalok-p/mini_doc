import random
import secrets
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.dependencies.auth import get_curr_user

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(payload: PaymentCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_curr_user)):
    result = await db.execute(
        select(Payment).where(
            Payment.idempotency_key == payload.idempotency_key,
            Payment.user_id == current_user.id,
        )
    )
    existing_payment = result.scalar_one_or_none()
    if existing_payment:
        return existing_payment

    # Validate booking
    result = await db.execute(
        select(Booking).where(
            Booking.id == payload.booking_id,
            Booking.user_id == current_user.id,
        )
    )
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status != "PENDING":
        raise HTTPException(status_code=400, detail="Payment can only be made for PENDING bookings")

    # Mock payment: 80% SUCCESS, 20% FAILED
    payment_status = "SUCCESS" if random.random() < 0.8 else "FAILED"
    transaction_ref = secrets.token_hex(16)

    payment = Payment(
        booking_id=booking.id,
        amount=booking.amount,
        status=payment_status,
        transaction_reference=transaction_ref,
        idempotency_key=payload.idempotency_key,
        user_id=current_user.id,
    )
    db.add(payment)

    # Update booking status on success
    if payment_status == "SUCCESS":
        booking.status = "CONFIRMED"
    await db.commit()
    await db.refresh(payment)
    return payment
