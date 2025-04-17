import click
from litestar import Litestar
from sqlalchemy import MetaData
from tabulate import tabulate

from messenger.lib.database import BaseModel


@click.command()
def show_database_schema(app: Litestar) -> None:
    BaseModel.metadata.create_all(app.settingsengine)

    m = MetaData()
    m.reflect(engine)

    rable_format = tabulate(
        [(table.name, [c.name for c in table.columns]) for table in m.tables.values()],
        headers=["Table", "Columns"],
    )

    print("Database schema:\n", rable_format)
