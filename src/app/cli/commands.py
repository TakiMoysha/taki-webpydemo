import click

from app.config.base import AppConfig
from app.lib.utils import get_random_string


@click.command()
def generate_env_file(settings: AppConfig): ...


@click.command()
def generate_secret_key(length: int) -> str:
    return get_random_string(length)


@click.command()
def check_server(settings: AppConfig): ...
