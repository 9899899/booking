"""booking time ranges must not overlap

Revision ID: c4a8e1b09f22
Revises: 926d30435549
Create Date: 2026-11-12 16:20:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = "c4a8e1b09f22"
down_revision: Union[str, Sequence[str], None] = "926d30435549"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.execute(
        """
        ALTER TABLE bookings
        ADD CONSTRAINT bookings_no_overlap
        EXCLUDE USING gist (
            room_id WITH =,
            tstzrange(start_time, end_time, '[)') WITH &&
        )
        WHERE (status = 'active')
        """
    )


def downgrade() -> None:
    op.execute("ALTER TABLE bookings DROP CONSTRAINT IF EXISTS bookings_no_overlap")
