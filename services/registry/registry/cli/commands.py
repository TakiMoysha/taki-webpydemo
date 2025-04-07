from registry import GLOBSCOPE
from tabulate import tabulate
import click

from registry.config import get_settings


@click.command
def status() -> None:
    print(
        f"Status\t\t{'OK'}",
    )


@click.command
def list_services() -> None:
    services_table = tabulate(
        [
            [
                service.name,
                service.address,
            ]
            for service in GLOBSCOPE.SERVICE_MAP
        ],
        headers=["Service", "Address"],
    )

    print(services_table)
