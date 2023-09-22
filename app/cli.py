import os

import click
from trogon import tui

from app.data.scripts.sync_req_files import sync_requirements_files as _sync_requirements_files
from app.data.scripts.update_all_data import update_all_data as _update_all_data
from app.data.scripts.update_test_data import update_test_data as _update_test_data
from app.docs.api_docs.readme import update_readme as _update_readme


@tui()
@click.group(name="util scripts")
def cli():
    pass


@cli.command()
def update_all_data():
    result = _update_all_data()
    exit_app(result, f'Updated database with data for Unicode version {os.environ.get("UNICODE_VERSION")}')


@cli.command()
def sync_req_files():
    result = _sync_requirements_files()
    exit_app(result, "Updated and synced all requirements files")


@cli.command()
def update_readme():
    result = _update_readme()
    exit_app(result, "Updated README.md")


@cli.command()
def update_test_data():
    result = _update_test_data()
    exit_app(result, "Updated data.py for test_get_character_details module.")


def exit_app(result, message=None):
    return exit_app_success(message) if result.success else exit_app_error(result.error)


def exit_app_success(message=None):
    if message:
        click.secho(message, fg="bright_green")
    return 0


def exit_app_error(message):
    if message:
        if isinstance(message, list):
            for m in message:
                click.secho(m, fg="bright_red")
        else:
            click.secho(message, fg="bright_red")
    return 1


if __name__ == "__main__":
    cli()
