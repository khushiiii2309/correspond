"""support user-editable category and priority

Revision ID: 9e02c5f4b348
Revises: 55b12d223e41
Create Date: 2026-11-18 23:34:35.752208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '9e02c5f4b348'
down_revision: Union[str, None] = '55b12d223e41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Preserve any existing AI classification data by renaming rather than
    # drop+add, and relax to nullable since an analysis row can now exist
    # purely from a user's manual classification before the AI ever ran.
    op.alter_column('email_analyses', 'category', new_column_name='ai_category', nullable=True)
    op.alter_column('email_analyses', 'priority', new_column_name='ai_priority', nullable=True)

    op.add_column(
        'email_analyses',
        sa.Column(
            'user_category',
            postgresql.ENUM(
                'IMPORTANT', 'REQUIRES_ACTION', 'INFORMATIONAL', 'PROMOTIONAL', 'POTENTIALLY_SUSPICIOUS',
                name='email_category', create_type=False,
            ),
            nullable=True,
        ),
    )
    op.add_column(
        'email_analyses',
        sa.Column(
            'user_priority',
            postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', name='priority_level', create_type=False),
            nullable=True,
        ),
    )

    op.add_column('email_analyses', sa.Column('category_overridden', sa.Boolean(), server_default=sa.false(), nullable=False))
    op.add_column('email_analyses', sa.Column('priority_overridden', sa.Boolean(), server_default=sa.false(), nullable=False))
    op.alter_column('email_analyses', 'category_overridden', server_default=None)
    op.alter_column('email_analyses', 'priority_overridden', server_default=None)


def downgrade() -> None:
    op.drop_column('email_analyses', 'priority_overridden')
    op.drop_column('email_analyses', 'category_overridden')
    op.drop_column('email_analyses', 'user_priority')
    op.drop_column('email_analyses', 'user_category')

    op.alter_column('email_analyses', 'ai_priority', new_column_name='priority', nullable=False)
    op.alter_column('email_analyses', 'ai_category', new_column_name='category', nullable=False)
