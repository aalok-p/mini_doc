"""add booking model
Revision ID: 20260929_add_booking
Revises: 20260929_add_diagnostic
Create Date: 2026-09-29 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '20260929_add_booking'
down_revision: Union[str, None] = '20260929_add_diagnostic'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'bookings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('test_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('diagnostic_tests.id'), nullable=False),
        sa.Column('centre_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('diagnostic_centres.id'), nullable=False),
        sa.Column('appointment_datetime', sa.DateTime(timezone=True), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('centre_id', 'test_id', 'appointment_datetime', name='uix_booking_slot')
    )

def downgrade() -> None:
    op.drop_table('bookings')
