import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class BookingCreate(BaseModel):
    test_id: str
    centre_id: str
    appointment_datetime: datetime


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    test_id: uuid.UUID
    centre_id: uuid.UUID
    appointment_datetime: datetime
    amount: Decimal
    status: str
    created_at: datetime
