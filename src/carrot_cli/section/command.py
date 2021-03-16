import logging
import sys

import click

from ..config import manager as config
from ..rest import sections, runs
from .. import file_util

LOGGER = logging.getLogger(__name__)


@click.group(name="section")
def main():
    """Commands for searching, creating, and updating sections"""


@main.command(name="find_by_id")
@click.argument("id")
def find_by_id(id):
    """Retrieve a section by its ID"""
    print(sections.find_by_id(id))


@main.command(name="find")
@click.option("--section_id", default="", help="The section's ID, a version 4 UUID")
@click.option("--name", default="", help="The name of the section, case-sensitive")
@click.option(
    "--description", default="", help="The description of the section, case-sensitive"
)
@click.option(
    "--contents",
    default="",
    help="An ipynb (or json) file containing the Jupyter notebook cells included in the section"
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for section's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for section's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the section, case sensitive",
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
    help="The maximum number of section records to return",
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
    section_id,
    name,
    description,
    contents,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset,
):
    """Retrieve sections filtered to match the specified parameters"""
    print(
        sections.find(
            section_id,
            name,
            description,
            file_util.read_file_to_json(contents),
            created_by,
            created_before,
            created_after,
            sort,
            limit,
            offset,
        )
    )


@main.command(name="create")
@click.option("--name", help="The name of the section", required=True)
@click.option("--description", default="", help="The description of the section")
@click.option(
    "--contents",
    default="",
    help="An ipynb (or json) file containing the Jupyter notebook cells to be included in the section",
    required=True
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the section.  Defaults to email config variable",
)
def create(name, description, contents, created_by):
    """Create section with the specified parameters"""
    # If created_by is not set and there is an email config variable, fill with that
    if created_by == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            created_by = email_config_val
        else:
            print(
                "No email config variable set.  If a value is not specified for --created by, "
                "there must be a value set for email."
            )
            sys.exit(1)
    print(sections.create(name, description, file_util.read_file_to_json(contents), created_by))


@main.command(name="update")
@click.argument("id")
@click.option("--name", default="", help="The name of the section")
@click.option("--description", default="", help="The description of the section")
@click.option(
    "--contents",
    default="",
    help="An ipynb (or json) file containing the Jupyter notebook cells to be included in the section"
)
def update(id, name, description, contents):
    """Update section with ID with the specified parameters"""
    print(sections.update(id, name, description, file_util.read_file_to_json(contents)))


@main.command(name="delete")
@click.argument("id")
def delete(id):
    """Delete a section by its ID, if the section is not mapped to a report"""
    print(sections.delete(id))

