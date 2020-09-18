import logging
import sys
import click

from ..config import manager as config
from ..rest import tests
from ..rest import runs

LOGGER = logging.getLogger(__name__)


@click.group(name="test")
def main():
    """Commands for searching, creating, and updating tests"""

@main.command(name="find_by_id")
@click.argument("id")
def find_by_id(id):
    """Retrieve a test by its ID"""
    print(tests.find_by_id(id))

@main.command(name="find")
@click.option(
    "--test_id",
    default="",
    help="The test's ID, a version 4 UUID"
)
@click.option(
    "--template_id",
    default="",
    help="The ID of the template that is the test's parent, a version 4 UUID"
)
@click.option(
    "--name",
    default="",
    help="The name of the test, case-sensitive"
)
@click.option(
    "--template_name",
    default="",
    help="The name of the template that is the test's parent, case-sensitive"
)
@click.option(
    "--description",
    default="",
    help="The description of the test, case-sensitive"
)
@click.option(
    "--test_input_defaults",
    default="",
    help="A JSON file containing the default inputs to the test WDL for the test"
)
@click.option(
    "--eval_input_defaults",
    default="",
    help="A JSON file containing the default inputs to the eval WDL for the test"
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for test's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for test's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the test, case sensitive"
)
@click.option(
    "--sort",
    default="",
    help="A comma-separated list of sort keys, enclosed in asc() for ascending or desc() for "
        "descending.  Ex. asc(name),desc(created_at)"
)
@click.option(
    "--limit",
    default=20,
    show_default=True,
    help="The maximum number of test records to return"
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
    test_id,
    template_id,
    name,
    template_name,
    description,
    test_input_defaults,
    eval_input_defaults,
    created_by,
    created_before,
    created_after,
    sort,
    limit,
    offset
):
    """Retrieve tests filtered to match the specified parameters"""
    # Load data from files for test_input_defaults and eval_input_defaults, if set
    if test_input_defaults != "":
        with open(test_input_defaults, 'r') as test_input_file:
            test_input_defaults = test_input_file.read()
    if eval_input_defaults != "":
        with open(eval_input_defaults, 'r') as eval_input_file:
            eval_input_defaults = eval_input_file.read()
    print(
        tests.find(
            test_id,
            template_id,
            name,
            template_name,
            description,
            test_input_defaults,
            eval_input_defaults,
            created_by,
            created_before,
            created_after,
            sort,
            limit,
            offset
        )
    )

@main.command(name="create")
@click.option(
    "--name",
    help="The name of the test",
    required=True
)
@click.option(
    "--template_id",
    required=True,
    help="The ID of the template that will be the test's parent, a version 4 UUID"
)
@click.option(
    "--description",
    default="",
    help="The description of the test"
)
@click.option(
    "--test_input_defaults",
    default="",
    help="A JSON file containing the default inputs to the test WDL for the test"
)
@click.option(
    "--eval_input_defaults",
    default="",
    help="A JSON file containing the default inputs to the eval WDL for the test"
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the test.  Defaults to email config variable"
)
def create(
    name,
    template_id,
    description,
    test_input_defaults,
    eval_input_defaults,
    created_by
):
    """Create test with the specified parameters"""
    # If created_by is not set and there is an email config variable, fill with that
    if created_by == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            created_by = email_config_val
    # Load data from files for test_input_defaults and eval_input_defaults, if set
    if test_input_defaults != "":
        with open(test_input_defaults, 'r') as test_input_file:
            test_input_defaults = test_input_file.read()
    if eval_input_defaults != "":
        with open(eval_input_defaults, 'r') as eval_input_file:
            eval_input_defaults = eval_input_file.read()
    print(
        tests.create(
            name,
            template_id,
            description,
            test_input_defaults,
            eval_input_defaults,
            created_by
        )
    )

@main.command(name="update")
@click.argument("id")
@click.option(
    "--name",
    default="",
    help="The name of the test"
)
@click.option(
    "--description",
    default="",
    help="The description of the test"
)
def update(
    id,
    name,
    description
):
    """Update test with ID with the specified parameters"""
    print(
        tests.update(
            id,
            name,
            description
        )
    )

@main.command(name="run")
@click.argument("id")
@click.option(
    "--name",
    default="",
    help="The name of the run.  Will be autogenerated if not specified"
)
@click.option(
    "--test_input",
    default="",
    help="A JSON file containing the inputs to the test WDL for the run"
)
@click.option(
    "--eval_input",
    default="",
    help="A JSON file containing the inputs to the eval WDL for the run"
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the run.  Defaults to email config variable"
)
def run(
    id,
    name,
    test_input,
    eval_input,
    created_by
):
    """Start a run for the test specified by ID with the specified params"""
    # If created_by is not set and there is an email config variable, fill with that
    if created_by == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            created_by = email_config_val
    # Load data from files for test_input and eval_input, if set
    if test_input != "":
        with open(test_input, 'r') as test_input_file:
            test_input = test_input_file.read()
    if eval_input != "":
        with open(eval_input, 'r') as eval_input_file:
            eval_input = eval_input_file.read()
    print(
        tests.run(
            id,
            name,
            test_input,
            eval_input,
            created_by
        )
    )

@main.command(name="find_runs")
@click.argument("id")
@click.option(
    "--name",
    default="",
    help="The name of the run"
)
@click.option(
    "--status",
    default="",
    help="The status of the run"
)
@click.option(
    "--test_input",
    default="",
    help="A JSON file containing the inputs to the test WDL for the run"
)
@click.option(
    "--eval_input",
    default="",
    help="A JSON file containing the inputs to the eval WDL for the run"
)
@click.option(
    "--cromwell_job_id",
    default="",
    help="The unique ID assigned to the Cromwell job in which the test ran"
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for run's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for run's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the run"
)
@click.option(
    "--finished_before",
    default="",
    help="Upper bound for run's finished_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--finished_after",
    default="",
    help="Lower bound for run's finished_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--sort",
    default="",
    help="A comma-separated list of sort keys, enclosed in asc() for ascending or desc() for "
        "descending.  Ex. asc(status),desc(created_at)"
)
@click.option(
    "--limit",
    default=20,
    show_default=True,
    help="The maximum number of run records to return"
)
@click.option(
    "--offset",
    default=0,
    show_default=True,
    help="The offset to start at within the list of records to return.  Ex. Sorting by "
        "asc(created_at) with offset=1 would return records sorted by when they were created "
        "starting from the second record to be created"
)
def find_runs(
    id,
    name,
    status,
    test_input,
    eval_input,
    cromwell_job_id,
    created_before,
    created_after,
    created_by,
    finished_before,
    finished_after,
    sort,
    limit,
    offset
):
    """Retrieve runs of the test specified by ID, filtered by the specified parameters"""
    # Load data from files for test_input and eval_input, if set
    if test_input != "":
        with open(test_input, 'r') as test_input_file:
            test_input = test_input_file.read()
    if eval_input != "":
        with open(eval_input, 'r') as eval_input_file:
            eval_input = eval_input_file.read()
    print(
        runs.find(
            "tests",
            id,
            name,
            status,
            test_input,
            eval_input,
            cromwell_job_id,
            created_before,
            created_after,
            created_by,
            finished_before,
            finished_after,
            sort,
            limit,
            offset
        )
    )

@main.command(name="subscribe")
@click.argument("id")
@click.option(
    "--email",
    default="",
    help="The email address to receive notifications. If set, takes priority over email config "
        "variable"
)
def subscribe(
    id,
    email
):
    """Subscribe to receive notifications about the test specified by ID"""
    # If email is not set and there is an email config variable, fill with that
    if email == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            email = email_config_val
        # If the config variable is also not set, print a message to the user and exit
        else:
            print("Subscribing requires that an email address is supplied either via the --email"
                "flag or by setting the email config variable")
            sys.exit(1)
    tests.subscribe(
        id,
        email
    )

@main.command(name="unsubscribe")
@click.argument("id")
@click.option(
    "--email",
    default="",
    help="The email address to stop receiving notifications. If set, takes priority over email "
        "config variable"
)
def unsubscribe(
    id,
    email
):
    """Delete subscription to the test with the specified by ID and email"""
    # If email is not set and there is an email config variable, fill with that
    if email == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            email = email_config_val
        # If the config variable is also not set, print a message to the user and exit
        else:
            print("Unsubscribing requires that an email address is supplied either via the --email"
                "flag or by setting the email config variable")
            sys.exit(1)
    tests.unsubscribe(
        id,
        email
    )
