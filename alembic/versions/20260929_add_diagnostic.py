"""add diagnostic models
Revision ID: 20260929_add_diagnostic
Revises: 20260929_add_user
Create Date: 2026-09-29 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '20260929_add_diagnostic'
down_revision: Union[str, None] = '20260929_add_user'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'diagnostic_centres',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('contact_phone', sa.String(), nullable=True),
        sa.Column('operating_hours', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'diagnostic_tests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('preparation_instructions', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'centre_tests',
        sa.Column('centre_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('test_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['centre_id'], ['diagnostic_centres.id']),
        sa.ForeignKeyConstraint(['test_id'], ['diagnostic_tests.id']),
        sa.PrimaryKeyConstraint('centre_id', 'test_id')
    )

def downgrade() -> None:
    op.drop_table('centre_tests')
    op.drop_table('diagnostic_tests')
    op.drop_table('diagnostic_centres')
