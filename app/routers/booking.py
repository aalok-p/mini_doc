from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.booking import Booking
from app.models.diagnostic import centre_tests
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.dependencies.auth import get_curr_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])
@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    payload: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_curr_user),
):
    if payload.appointment_datetime < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Appointment date must be in the future")

    result = await db.execute(
        select(centre_tests.c.price).where(
            centre_tests.c.centre_id == payload.centre_id,
            centre_tests.c.test_id == payload.test_id,
        )
    )
    price = result.scalar_one_or_none()
    if price is None:
        raise HTTPException(status_code=400, detail="Test not available at this centre")

    booking = Booking(
        user_id=current_user.id,
        test_id=payload.test_id,
        centre_id=payload.centre_id,
        appointment_datetime=payload.appointment_datetime,
        amount=Decimal(str(price)),
        status="PENDING",
    )
    db.add(booking)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="This slot is already booked")
    await db.refresh(booking)
    return booking

@router.get("", response_model=list[BookingResponse])
async def list_bookings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_curr_user),
):
    result = await db.execute(
        select(Booking).where(Booking.user_id == current_user.id)
    )
    return result.scalars().all()

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_curr_user),
):
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id, Booking.user_id == current_user.id)
    )
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    booking_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_curr_user),
):
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id, Booking.user_id == current_user.id)
    )
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Booking already cancelled")

    booking.status = "CANCELLED"
    await db.commit()
    await db.refresh(booking)
    return booking
