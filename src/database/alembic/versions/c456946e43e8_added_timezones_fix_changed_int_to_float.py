"""added timezones; fix changed int to float

Revision ID: c456946e43e8
Revises: 4949a9d30aaa
Create Date: 2025-03-16 00:07:46.056364

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c456946e43e8'
down_revision: Union[str, None] = '4949a9d30aaa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Coil', 'length',
               existing_type=sa.BIGINT(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('Coil', 'weight',
               existing_type=sa.BIGINT(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('Coil', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    op.alter_column('Coil', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Coil', 'deleted_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('Coil', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('Coil', 'weight',
               existing_type=sa.Float(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('Coil', 'length',
               existing_type=sa.Float(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    # ### end Alembic commands ###
