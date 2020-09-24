import logging
import click

from ..rest import runs

LOGGER = logging.getLogger(__name__)

@click.group(name="run")
def main():
    """Commands for searching, creating, and updating runs"""

@main.command(name="find_by_id")
@click.argument("id")
def find_by_id(id):
    """Retrieve a run by its ID"""
    print(runs.find_by_id(id))