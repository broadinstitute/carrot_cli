import logging
import click

from ...rest import software_versions
from .software_build import command as software_build

LOGGER = logging.getLogger(__name__)

@click.group(name="version")
def main():
    "Commands for querying software version records"

@main.command(name="find_by_id")
@click.argument("id")
def find_by_id(id):
    """Retrieve a software version record by its ID"""
    print(software_versions.find_by_id(id))

@main.command(name="find")
@click.option(
    "--software_version_id",
    default="",
    help="The ID of the software version record, a version 4 UUID"
)
@click.option(
    "--software_id",
    default="",
    help="The ID of the software to find version records of, a version 4 UUID"
)
@click.option(
    "--commit",
    default="",
    help="The commit hash for the version"
)
@click.option(
    "--software_name",
    default="",
    help="The name of the software to find version records of, case-sensitive"
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for software version's created_at value, in the format "
        "YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for software version's created_at value, in the format "
        "YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--sort",
    default="",
    help="A comma-separated list of sort keys, enclosed in asc() for ascending or desc() for "
        "descending.  Ex. asc(software_name),desc(created_at)"
)
@click.option(
    "--limit",
    default=20,
    show_default=True,
    help="The maximum number of software version records to return"
)
@click.option(
    "--offset",
    default=0,
    show_default=True,
    help="The offset to start at within the list of records to return.  Ex. Sorting by "
        "asc(created_at) with offset=1 would return records sorted by when they were created "
        "starting from the second record to be created"
)
def find(
    software_version_id,
    software_id,
    commit,
    software_name,
    created_before,
    created_after,
    sort,
    limit,
    offset
):
    """Retrieve software version records filtered to match the specified parameters"""
    print(
        software_versions.find(
            software_version_id,
            software_id,
            commit,
            software_name,
            created_before,
            created_after,
            sort,
            limit,
            offset
        )
    )

main.add_command(software_build.main)
