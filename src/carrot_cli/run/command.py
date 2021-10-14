import json
import logging
import sys

import click

from .. import file_util
from ..config import manager as config
from ..rest import run_reports, runs

LOGGER = logging.getLogger(__name__)


@click.group(name="run")
def main():
    """Commands for searching, creating, and updating runs"""


@main.command(name="find_by_id")
@click.argument("id")
def find_by_id(id):
    """Retrieve a run by its ID"""
    print(runs.find_by_id(id))


@main.command(name="delete")
@click.argument("id")
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Automatically answers yes if prompted to confirm delete of run created by "
    "another user",
)
def delete(id, yes):
    """Delete a run by its ID, if the run has a failed status"""
    # Unless user specifies --yes flag, check first to see if the record exists and prompt to user to confirm delete if
    # they are not the creator
    if not yes:
        # Try to find the record by id
        record = json.loads(runs.find_by_id(id))
        # If the returned record has a created_by field that does not match the user email, prompt the user to confirm
        # the delete
        user_email = config.load_var("email")
        if "created_by" in record and record["created_by"] != user_email:
            # If they decide not to delete, exit
            if not click.confirm(
                f"Run with id {id} was created by {record['created_by']}. Are you sure you want to delete?"
            ):
                LOGGER.info("Okay, aborting delete operation")
                sys.exit(0)

    print(runs.delete(id))


@main.command(name="create_report")
@click.argument("id")
@click.argument("report_id")
@click.option("--created_by", default="", help="Email of the creator of the mapping")
@click.option(
    "--delete_failed",
    is_flag=True,
    help="If set, and there is a failed record for this run with this report, will overwrite that "
    "record",
)
def create_report(id, report_id, created_by, delete_failed):
    """
    Start a job to generate a filled report using data from the run specified by ID with the
    report specified by REPORT_ID
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
    print(run_reports.create_map(id, report_id, created_by, delete_failed))


@main.command(name="find_report_by_ids")
@click.argument("id")
@click.argument("report_id")
def find_report_by_ids(id, report_id):
    """
    Retrieve the report record for the run specified by ID and the report specified by
    REPORT_ID
    """
    print(run_reports.find_map_by_ids(id, report_id))


@main.command(name="find_reports")
@click.argument("id")
@click.option("--report_id", default="", help="The id of the report")
@click.option(
    "--status", default="", help="The status of the job generating the report"
)
@click.option(
    "--cromwell_job_id",
    default="",
    help="The id for the cromwell job for generating the filled report",
)
@click.option(
    "--results",
    default="",
    help="A json file containing the results of the report job",
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for report record's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for report record's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the report record, case sensitive",
)
@click.option(
    "--finished_before",
    default="",
    help="Upper bound for report record's finished_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--finished_after",
    default="",
    help="Lower bound for report record's finished_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--sort",
    default="",
    help="A comma-separated list of sort keys, enclosed in asc() for ascending or desc() for "
    "descending.  Ex. asc(input_map),desc(report_id)",
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
def find_reports(
    id,
    report_id,
    status,
    cromwell_job_id,
    results,
    created_before,
    created_after,
    created_by,
    finished_before,
    finished_after,
    sort,
    limit,
    offset,
):
    """
    Retrieve the report record from the run specified by ID for the report specified by
    REPORT_ID
    """
    print(
        run_reports.find_maps(
            id,
            report_id,
            status,
            cromwell_job_id,
            file_util.read_file_to_json(results),
            created_before,
            created_after,
            created_by,
            finished_before,
            finished_after,
            sort,
            limit,
            offset,
        )
    )


@main.command(name="delete_report_by_ids")
@click.argument("id")
@click.argument("report_id")
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Automatically answers yes if prompted to confirm delete of report created by "
    "another user",
)
def delete_report_by_ids(id, report_id, yes):
    """
    Delete the report record for the run specified by ID to the report specified by
    REPORT_ID
    """
    # Unless user specifies --yes flag, check first to see if the record exists and prompt to user to confirm delete if
    # they are not the creator
    if not yes:
        # Try to find the record by id
        record = json.loads(run_reports.find_map_by_ids(id, report_id))
        # If the returned record has a created_by field that does not match the user email, prompt the user to confirm
        # the delete
        user_email = config.load_var("email")
        if "created_by" in record and record["created_by"] != user_email:
            # If they decide not to delete, exit
            if not click.confirm(
                f"Run report for run with id {id} and report with id {report_id} was created by "
                f"{record['created_by']}. Are you sure you want to delete?"
            ):
                LOGGER.info("Okay, aborting delete operation")
                sys.exit(0)

    print(run_reports.delete_map_by_ids(id, report_id))
