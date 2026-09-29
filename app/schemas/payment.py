import uuid
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class PaymentCreate(BaseModel):
    booking_id: str
    idempotency_key: str

class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    booking_id: uuid.UUID
    amount: Decimal
    status: str
    transaction_reference: str
