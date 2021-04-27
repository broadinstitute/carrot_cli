import logging
import sys

import click

from .. import file_util
from ..config import manager as config
from ..rest import runs, template_reports, template_results, templates

LOGGER = logging.getLogger(__name__)


@click.group(name="template")
def main():
    """Commands for searching, creating, and updating templates"""


@main.command(name="find_by_id")
@click.argument("id")
def find_by_id(id):
    """Retrieve a template by its ID"""
    print(templates.find_by_id(id))


@main.command(name="find")
@click.option("--template_id", default="", help="The template's ID, a version 4 UUID")
@click.option(
    "--pipeline_id",
    default="",
    help="The ID of the pipeline that is the template's parent, a version 4 UUID",
)
@click.option("--name", default="", help="The name of the template, case-sensitive")
@click.option(
    "--pipeline_name",
    default="",
    help="The name of the pipeline that is the template's parent, case-sensitive",
)
@click.option(
    "--description", default="", help="The description of the template, case-sensitive"
)
@click.option(
    "--test_wdl",
    default="",
    help="The location where the test WDL for the template is hosted",
)
@click.option(
    "--eval_wdl",
    default="",
    help="The location where the eval WDL for the template is hosted",
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for template's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for template's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the template, case sensitive",
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
    help="The maximum number of template records to return",
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
    template_id,
    pipeline_id,
    name,
    pipeline_name,
    description,
    test_wdl,
    eval_wdl,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset,
):
    """Retrieve templates filtered to match the specified parameters"""
    print(
        templates.find(
            template_id,
            pipeline_id,
            name,
            pipeline_name,
            description,
            test_wdl,
            eval_wdl,
            created_by,
            created_before,
            created_after,
            sort,
            limit,
            offset,
        )
    )


@main.command(name="create")
@click.option(
    "--pipeline_id",
    help="The ID of the pipeline that will be this template's parent",
    required=True,
)
@click.option("--name", help="The name of the template", required=True)
@click.option("--description", default="", help="The description of the template")
@click.option(
    "--test_wdl",
    required=True,
    help="The location where the test WDL for this template is hosted. The test WDL is the WDL "
    "which defines the thing the be tested",
)
@click.option(
    "--eval_wdl",
    required=True,
    help="The location where the eval WDL for ths template is hosted.  The eval WDL is the WDL "
    "which takes the outputs from the test WDL and evaluates them",
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the template.  Defaults to email config variable",
)
def create(name, pipeline_id, description, test_wdl, eval_wdl, created_by):
    """Create template with the specified parameters"""
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
        templates.create(name, pipeline_id, description, test_wdl, eval_wdl, created_by)
    )


@main.command(name="update")
@click.argument("id")
@click.option("--name", default="", help="The name of the template")
@click.option("--description", default="", help="The description of the template")
@click.option(
    "--test_wdl",
    default="",
    help="The location where the test WDL for the template is hosted.  Updating this parameter "
    "is allowed only if the specified template has no non-failed (i.e. successful or currently "
    "running) runs associated with it",
)
@click.option(
    "--eval_wdl",
    default="",
    help="The location where the eval WDL for the template is hosted.  Updating this parameter "
    "is allowed only if the specified template has no non-failed (i.e. successful or currently "
    "running) runs associated with it",
)
def update(id, name, description, test_wdl, eval_wdl):
    """Update template with ID with the specified parameters"""
    print(templates.update(id, name, description, test_wdl, eval_wdl))


@main.command(name="delete")
@click.argument("id")
def delete(id):
    """Delete a template by its ID, if it has no tests associated with it"""
    print(templates.delete(id))


@main.command(name="find_runs")
@click.argument("id")
@click.option("--name", default="", help="The name of the run")
@click.option(
    "--status",
    default="",
    help="The status of the run. Status include: aborted, building, created, failed, "
    "queued_in_cromwell, running, starting, submitted, succeeded, waiting_for_queue_space",
)
@click.option(
    "--test_input",
    default="",
    help="A JSON file containing the inputs to the test WDL for the run",
)
@click.option(
    "--eval_input",
    default="",
    help="A JSON file containing the inputs to the eval WDL for the run",
)
@click.option(
    "--test_cromwell_job_id",
    default="",
    help="The unique ID assigned to the Cromwell job in which the test WDL ran",
)
@click.option(
    "--eval_cromwell_job_id",
    default="",
    help="The unique ID assigned to the Cromwell job in which the eval WDL ran",
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for run's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for run's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option("--created_by", default="", help="Email of the creator of the run")
@click.option(
    "--finished_before",
    default="",
    help="Upper bound for run's finished_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--finished_after",
    default="",
    help="Lower bound for run's finished_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss",
)
@click.option(
    "--sort",
    default="",
    help="A comma-separated list of sort keys, enclosed in asc() for ascending or desc() for "
    "descending.  Ex. asc(status),desc(created_at)",
)
@click.option(
    "--limit",
    default=20,
    show_default=True,
    help="The maximum number of run records to return",
)
@click.option(
    "--offset",
    default=0,
    show_default=True,
    help="The offset to start at within the list of records to return.  Ex. Sorting by "
    "asc(created_at) with offset=1 would return records sorted by when they were created "
    "starting from the second record to be created",
)
def find_runs(
    id,
    name,
    status,
    test_input,
    eval_input,
    test_cromwell_job_id,
    eval_cromwell_job_id,
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
    Retrieve runs related to the template specified by ID, filtered by the specified parameters
    """
    # Load data from files for test_input and eval_input, if set
    test_input = file_util.read_file_to_json(test_input)
    eval_input = file_util.read_file_to_json(eval_input)
    print(
        runs.find(
            "templates",
            id,
            name,
            status,
            test_input,
            eval_input,
            test_cromwell_job_id,
            eval_cromwell_job_id,
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


@main.command(name="subscribe")
@click.argument("id")
@click.option(
    "--email",
    default="",
    help="The email address to receive notifications. If set, takes priority over email config "
    "variable",
)
def subscribe(id, email):
    """Subscribe to receive notifications about the template specified by ID"""
    # If email is not set and there is an email config variable, fill with that
    if email == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            email = email_config_val
        # If the config variable is also not set, print a message to the user and exit
        else:
            print(
                "Subscribing requires that an email address is supplied either via the --email"
                "flag or by setting the email config variable"
            )
            sys.exit(1)
    print(templates.subscribe(id, email))


@main.command(name="unsubscribe")
@click.argument("id")
@click.option(
    "--email",
    default="",
    help="The email address to stop receiving notifications. If set, takes priority over email "
    "config variable",
)
def unsubscribe(id, email):
    """Delete subscription to the template with the specified by ID and email"""
    # If email is not set and there is an email config variable, fill with that
    if email == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            email = email_config_val
        # If the config variable is also not set, print a message to the user and exit
        else:
            print(
                "Unsubscribing requires that an email address is supplied either via the --email"
                "flag or by setting the email config variable"
            )
            sys.exit(1)
    print(templates.unsubscribe(id, email))


@main.command(name="map_to_result")
@click.argument("id")
@click.argument("result_id")
@click.argument("result_key")
@click.option("--created_by", default="", help="Email of the creator of the mapping")
def map_to_result(id, result_id, result_key, created_by):
    """
    Map the template specified by ID to the result specified by RESULT_ID for RESULT_KEY in
    in the output generated by that template
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
    print(template_results.create_map(id, result_id, result_key, created_by))


@main.command(name="find_result_map_by_id")
@click.argument("id")
@click.argument("result_id")
def find_result_map_by_id(id, result_id):
    """
    Retrieve the mapping record from the template specified by ID to the result specified by
    RESULT_ID
    """
    print(template_results.find_map_by_ids(id, result_id))


@main.command(name="find_result_maps")
@click.argument("id")
@click.option("--result_id", default="", help="The id of the result")
@click.option(
    "--result_key",
    default="",
    help="The key used to name the result within the output of the template",
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
    "descending.  Ex. asc(result_key),desc(result_id)",
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
def find_result_maps(
    id,
    result_id,
    result_key,
    created_before,
    created_after,
    created_by,
    sort,
    limit,
    offset,
):
    """
    Retrieve the mapping record from the template specified by ID to the result specified by
    RESULT_ID
    """
    print(
        template_results.find_maps(
            id,
            result_id,
            result_key,
            created_before,
            created_after,
            created_by,
            sort,
            limit,
            offset,
        )
    )


@main.command(name="delete_result_map_by_id")
@click.argument("id")
@click.argument("result_id")
def delete_result_map_by_id(id, result_id):
    """
    Delete the mapping record from the template specified by ID to the result specified by
    RESULT_ID, if the specified template has no non-failed (i.e. successful or currently running)
    runs associated with it
    """
    print(template_results.delete_map_by_ids(id, result_id))


@main.command(name="map_to_report")
@click.argument("id")
@click.argument("report_id")
@click.option("--created_by", default="", help="Email of the creator of the mapping")
def map_to_report(id, report_id, created_by):
    """
    Map the template specified by ID to the report specified by REPORT_ID
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
    print(template_reports.create_map(id, report_id, created_by))


@main.command(name="find_report_map_by_id")
@click.argument("id")
@click.argument("report_id")
def find_report_map_by_id(id, report_id):
    """
    Retrieve the mapping record from the template specified by ID to the report specified by
    REPORT_ID
    """
    print(template_reports.find_map_by_ids(id, report_id))


@main.command(name="find_report_maps")
@click.argument("id")
@click.option("--report_id", default="", help="The id of the report")
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
def find_report_maps(
    id,
    report_id,
    created_before,
    created_after,
    created_by,
    sort,
    limit,
    offset,
):
    """
    Retrieve the mapping record from the template specified by ID to the report specified by
    REPORT_ID
    """
    print(
        template_reports.find_maps(
            id,
            report_id,
            created_before,
            created_after,
            created_by,
            sort,
            limit,
            offset,
        )
    )


@main.command(name="delete_report_map_by_id")
@click.argument("id")
@click.argument("report_id")
def delete_report_map_by_id(id, report_id):
    """
    Delete the mapping record from the template specified by ID to the report specified by
    REPORT_ID, if the specified template has no non-failed (i.e. successful or currently running)
    runs associated with it
    """
    print(template_reports.delete_map_by_ids(id, report_id))
