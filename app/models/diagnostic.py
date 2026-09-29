import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Numeric, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class DiagnosticCentre(Base):
    __tablename__ = "diagnostic_centres"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    operating_hours = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    tests = relationship("DiagnosticTest", secondary="centre_tests", back_populates="centres")


class DiagnosticTest(Base):
    __tablename__ = "diagnostic_tests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    preparation_instructions = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    centres = relationship("DiagnosticCentre", secondary="centre_tests", back_populates="tests")


centre_tests = Table(
    "centre_tests",
    Base.metadata,
    Column("centre_id", UUID(as_uuid=True), ForeignKey("diagnostic_centres.id"), primary_key=True),
    Column("test_id", UUID(as_uuid=True), ForeignKey("diagnostic_tests.id"), primary_key=True),
    Column("price", Numeric(10, 2), nullable=False),
    Column("duration_minutes", Integer, nullable=False),
)
