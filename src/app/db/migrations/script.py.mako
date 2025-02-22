# type: ignore
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Union, Sequence

import warnings
import sqlalchemy as sa
import advanced_alchemy

from alembic import op
from sqlalchemy import Text
from advanced_alchemy.types import GUID, ORA_JSONB, DateTimeUTC, EncryptedText, EncryptedString

${imports if imports else ""}

__all__ = [
  "downgrade",
  "upgrade",
  "schema_upgrades",
  "schema_downgrades",
  "data_upgrades",
  "data_downgrades",
]

sa.GUID = GUID
sa.DateTimeUTC = DateTimeUTC
sa.ORA_JSONB = ORA_JSONB
sa.EncryptedString = EncryptedString
sa.EncryptedText = EncryptedText

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            schema_upgrades()
            data_upgrades()


def downgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            data_downgrades()
            schema_downgrades()


def schema_upgrades() -> None:
    ${upgrades if upgrades else "pass"}


def schema_downgrades() -> None:
    ${downgrades if downgrades else "pass"}


def data_upgrades() -> None:
    """Space for additional migrations when updating data"""


def data_downgrades() -> None:
    """Space for additional migrations when downgrades data"""
