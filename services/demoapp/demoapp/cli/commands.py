import click

from litestar import Litestar


@click.command()
def show_database_schema(app: Litestar) -> None: ...
