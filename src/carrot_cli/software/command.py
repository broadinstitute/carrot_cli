import logging

import click

from ..config import manager as config
from ..rest import software
from .software_version import command as software_version

LOGGER = logging.getLogger(__name__)


@click.group(name="software")
def main():
    """Commands for searching, creating, and updating software definitions"""


@main.command(name="find_by_id")
@click.argument("id")
def find_by_id(id):
    """Retrieve a software definition by its ID"""
    print(software.find_by_id(id))


@main.command(name="find")
@click.option("--software_id", default="", help="The software's ID, a version 4 UUID")
@click.option("--name", default="", help="The name of the software, case-sensitive")
@click.option(
    "--description", default="", help="The description of the software, case-sensitive"
)
@click.option(
    "--repository_url",
    default="",
    help="The url of the repository where the software code is hosted",
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for software's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for software's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the software, case sensitive",
)
@click.option(
    "--sort",
    default="",
    help="A comma-separated list of sort keys, enclosed in asc() for ascending or desc() for "
    "descending.  Ex. asc(name),desc(created_at)",
)
@click.option(
    "--limit",
    default=20,
    show_default=True,
    help="The maximum number of software records to return",
)
@click.option(
    "--offset",
    default=0,
    show_default=True,
    help="The offset to start at within the list of records to return.  Ex. Sorting by "
    "asc(created_at) with offset=1 would return records sorted by when they were created "
    "starting from the second record to be created",
)
def find(
    software_id,
    name,
    description,
    repository_url,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset,
):
    """Retrieve software definitions filtered to match the specified parameters"""
    print(
        software.find(
            software_id,
            name,
            description,
            repository_url,
            created_by,
            created_before,
            created_after,
            sort,
            limit,
            offset,
        )
    )


@main.command(name="create")
@click.option("--name", help="The name of the software", required=True)
@click.option("--description", default="", help="The description of the software")
@click.option(
    "--repository_url",
    default="",
    help="The url to use for cloning the repository.",
    required=True,
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the software.  Defaults to email config variable",
)
def create(name, description, repository_url, created_by):
    """Create software definition with the specified parameters"""
    # If created_by is not set and there is an email config variable, fill with that
    if created_by == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            created_by = email_config_val
    print(software.create(name, description, repository_url, created_by))


@main.command(name="update")
@click.argument("id")
@click.option("--name", default="", help="The name of the software")
@click.option("--description", default="", help="The description of the software")
def update(id, name, description):
    """Update software definition with ID with the specified parameters"""
    print(software.update(id, name, description))


main.add_command(software_version.main)
