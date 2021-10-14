import json
import logging
import sys

import click

from ..config import manager as config
from ..rest import results, template_results

LOGGER = logging.getLogger(__name__)


@click.group(name="result")
def main():
    """Commands for searching, creating, and updating result definitions"""


@main.command(name="find_by_id")
@click.argument("id")
def find_by_id(id):
    """Retrieve a result definition by its ID"""
    print(results.find_by_id(id))


@main.command(name="find")
@click.option("--result_id", default="", help="The result's ID, a version 4 UUID")
@click.option("--name", default="", help="The name of the result, case-sensitive")
@click.option(
    "--description", default="", help="The description of the result, case-sensitive"
)
@click.option(
    "--result_type", default="", help="The type of the result: numeric, file, or text"
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for result's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for result's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the result, case-sensitive",
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
    help="The maximum number of result records to return",
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
    result_id,
    name,
    description,
    result_type,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset,
):
    """Retrieve results filtered to match the specified parameters"""
    print(
        results.find(
            result_id,
            name,
            description,
            result_type,
            created_by,
            created_before,
            created_after,
            sort,
            limit,
            offset,
        )
    )


@main.command(name="create")
@click.option("--name", help="The name of the result", required=True)
@click.option("--description", default="", help="The description of the result")
@click.option(
    "--result_type",
    help="The type of the result: numeric, file, or text",
    required=True,
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the result.  Defaults to email config variable",
)
def create(name, description, result_type, created_by):
    """Create result with the specified parameters"""
    # If created_by is not set and there is an email config variable, fill with that
    if created_by == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            created_by = email_config_val
        else:
            LOGGER.error(
                "No email config variable set.  If a value is not specified for --created by, "
                "there must be a value set for email."
            )
            sys.exit(1)
    print(results.create(name, description, result_type, created_by))


@main.command(name="update")
@click.argument("id")
@click.option("--name", default="", help="The name of the result")
@click.option("--description", default="", help="The description of the result")
def update(id, name, description):
    """Update result with ID with the specified parameters"""
    print(results.update(id, name, description))


@main.command(name="delete")
@click.argument("id")
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Automatically answers yes if prompted to confirm delete of result created by "
    "another user",
)
def delete(id, yes):
    """Delete a result definition by its ID, if the result is not mapped to any templates"""
    # Unless user specifies --yes flag, check first to see if the record exists and prompt to user to confirm delete if
    # they are not the creator
    if not yes:
        # Try to find the record by id
        record = json.loads(results.find_by_id(id))
        # If the returned record has a created_by field that does not match the user email, prompt the user to confirm
        # the delete
        user_email = config.load_var("email")
        if "created_by" in record and record["created_by"] != user_email:
            # If they decide not to delete, exit
            if not click.confirm(
                f"Result with id {id} was created by {record['created_by']}. Are you sure you want to delete?"
            ):
                LOGGER.info("Okay, aborting delete operation")
                sys.exit(0)

    print(results.delete(id))


@main.command(name="map_to_template")
@click.argument("id")
@click.argument("template_id")
@click.argument("result_key")
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the mapping.  Defaults to email config variable",
)
def map_to_template(id, template_id, result_key, created_by):
    """
    Map the result specified by ID to the template specified by TEMPLATE_ID for RESULT_KEY in
    in the output generated by that template
    """
    # If created_by is not set and there is an email config variable, fill with that
    if created_by == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            created_by = email_config_val
        else:
            LOGGER.error(
                "No email config variable set.  If a value is not specified for --created by, "
                "there must be a value set for email."
            )
            sys.exit(1)
    print(template_results.create_map(template_id, id, result_key, created_by))
