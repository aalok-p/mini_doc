import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DiagnosticCentreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    location: str
    city: str
    address: str | None
    contact_phone: str | None
    operating_hours: str | None


class DiagnosticTestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    preparation_instructions: str | None


class CentreTestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    preparation_instructions: str | None
    price: Decimal
    duration_minutes: int
