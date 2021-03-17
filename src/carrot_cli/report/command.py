import logging
import sys

import click

from ..config import manager as config
from ..rest import reports, report_sections
from .. import file_util

LOGGER = logging.getLogger(__name__)


@click.group(name="report")
def main():
    """Commands for searching, creating, and updating reports"""


@main.command(name="find_by_id")
@click.argument("id")
def find_by_id(id):
    """Retrieve a report by its ID"""
    print(reports.find_by_id(id))


@main.command(name="find")
@click.option("--report_id", default="", help="The report's ID, a version 4 UUID")
@click.option("--name", default="", help="The name of the report, case-sensitive")
@click.option(
    "--description", default="", help="The description of the report, case-sensitive"
)
@click.option(
    "--metadata",
    default="",
    help="The JSON file containing ipynb metadata (non-'cells') attributes for the report"
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for report's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for report's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the report, case sensitive",
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
    help="The maximum number of report records to return",
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
    report_id,
    name,
    description,
    metadata,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset,
):
    """Retrieve reports filtered to match the specified parameters"""
    print(
        reports.find(
            report_id,
            name,
            description,
            file_util.read_file_to_json(metadata),
            created_by,
            created_before,
            created_after,
            sort,
            limit,
            offset,
        )
    )


@main.command(name="create")
@click.option("--name", help="The name of the report", required=True)
@click.option("--description", default="", help="The description of the report")
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the report.  Defaults to email config variable",
)
def create(name, description, created_by):
    """Create report with the specified parameters"""
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
    print(reports.create(name, description, created_by))


@main.command(name="update")
@click.argument("id")
@click.option("--name", default="", help="The name of the report")
@click.option("--description", default="", help="The description of the report")
def update(id, name, description):
    """Update report with ID with the specified parameters"""
    print(reports.update(id, name, description))


@main.command(name="delete")
@click.argument("id")
def delete(id):
    """Delete a report by its ID, if the report has no templates, sections, or runs associated with it."""
    print(reports.delete(id))

@main.command(name="map_to_section")
@click.argument("id")
@click.argument("section_id")
@click.argument("name")
@click.argument("position")
@click.option("--created_by", default="", help="Email of the creator of the mapping")
def map_to_section(id, section_id, name, position, created_by):
    """
    Map the report specified by ID to the section specified by SECTION_ID, so that section will
    appear at position POSITION within the report, named NAME
    """
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
    print(
        report_sections.create_map(
            id,
            section_id,
            name,
            position,
            created_by
        )
    )

@main.command(name="find_section_map_by_ids_and_name")
@click.argument("id")
@click.argument("section_id")
@click.argument("name")
def find_section_map_by_ids_and_name(id, section_id, name):
    """
    Retrieve the mapping record from the report specified by ID to the section specified by
    SECTION_ID, where the name of the section within the report is NAME
    """
    print(report_sections.find_map_by_ids_and_name(id, section_id, name))

@main.command(name="delete_section_map_by_ids_and_name")
@click.argument("id")
@click.argument("section_id")
@click.argument("name")
def delete_section_map_by_ids_and_name(id, section_id, name):
    """
    Delete the mapping record from the report specified by ID to the section specified by
    SECTION_ID, where the name of the section within the report is NAME
    """
    print(report_sections.delete_map_by_ids_and_name(id, section_id, name))

@main.command(name="find_section_maps")
@click.argument("id")
@click.option("--section_id", default="", help="The id of the section")
@click.option(
    "--name",
    default="",
    help="The name used for the section within the report",
)
@click.option(
    "--position",
    default="",
    help="The position at which the section appears in the report",
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for map's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for map's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_by", default="", help="Email of the creator of the map, case sensitive"
)
@click.option(
    "--sort",
    default="",
    help="A comma-separated list of sort keys, enclosed in asc() for ascending or desc() for "
    "descending.  Ex. asc(report_id),desc(position)",
)
@click.option(
    "--limit",
    default=20,
    show_default=True,
    help="The maximum number of map records to return",
)
@click.option(
    "--offset",
    default=0,
    show_default=True,
    help="The offset to start at within the list of records to return.  Ex. Sorting by "
    "asc(created_at) with offset=1 would return records sorted by when they were created "
    "starting from the second record to be created",
)
def find_section_maps(
    id,
    section_id,
    name,
    position,
    created_before,
    created_after,
    created_by,
    sort,
    limit,
    offset,
):
    """
    Retrieve the mapping records from the report specified by ID, with the specified parameters
    """
    print(
        report_sections.find_maps(
            id,
            section_id,
            name,
            position,
            created_before,
            created_after,
            created_by,
            sort,
            limit,
            offset,
        )
    )
