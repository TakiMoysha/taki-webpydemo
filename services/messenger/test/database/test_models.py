from tabulate import tabulate
import pytest
from sqlalchemy import Connection, MetaData
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, SessionEvents
from sqlalchemy_utils import database_exists

from messenger.database.models import User
from messenger.lib.database import BaseModel

from sqlalchemy.engine.reflection import Inspector


@pytest.mark.tdd
def test_database_schema(engine: Engine) -> None:
    BaseModel.metadata.create_all(engine)

    m = MetaData()
    m.reflect(engine)

    rable_format = tabulate(
        [(table.name, [c.name for c in table.columns]) for table in m.tables.values()],
        headers=["Table", "Columns"],
    )

    print("Database schema:\n", rable_format)
