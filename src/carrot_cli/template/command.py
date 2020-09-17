import logging
import sys
import click

from ..config import manager as config
from ..rest import templates

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
@click.option(
    "--template_id",
    default="",
    help="The template's ID, a version 4 UUID"
)
@click.option(
    "--pipeline_id",
    default="",
    help="The ID of the pipeline that is the template's parent, a version 4 UUID"
)
@click.option(
    "--name",
    default="",
    help="The name of the template, case-sensitive"
)
@click.option(
    "--pipeline_name",
    default="",
    help="The name of the pipeline that is the template's parent, case-sensitive"
)
@click.option(
    "--description",
    default="",
    help="The description of the template, case-sensitive"
)
@click.option(
    "--test_wdl",
    default="",
    help="The location where the test WDL for the template is hosted"
)
@click.option(
    "--eval_wdl",
    default="",
    help="The location where the eval WDL for the template is hosted"
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for template's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for template's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the template, case sensitive"
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
    help="The maximum number of template records to return"
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
    offset
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
            offset
    ))

@main.command(name="create")
@click.option(
    "--pipeline_id",
    help="The ID of the pipeline that will be this template's parent",
    required=True
)
@click.option(
    "--name",
    help="The name of the template",
    required=True
)
@click.option(
    "--description",
    default="",
    help="The description of the template"
)
@click.option(
    "--test_wdl",
    required=True,
    help="The location where the test WDL for this template is hosted. The test WDL is the WDL "
        "which defines the thing the be tested"
)
@click.option(
    "--eval_wdl",
    required=True,
    help="The location where the eval WDL for ths template is hosted.  The eval WDL is the WDL "
        "which takes the outputs from the test WDL and evaluates them"
)
@click.option(
    "--created_by",
    default="",
    help="Email of the creator of the template.  Defaults to email config variable"
)
def create(
    name,
    pipeline_id,
    description,
    test_wdl,
    eval_wdl,
    created_by
):
    """Create template with the specified parameters"""
    # If created_by is not set and there is an email config variable, fill with that
    if created_by == "":
        email_config_val = config.load_var_no_error("email")
        if email_config_val is not None:
            created_by = email_config_val
    print(
        templates.create(
            name,
            pipeline_id,
            description,
            test_wdl,
            eval_wdl,
            created_by
        )
    )

@main.command(name="update")
@click.argument("id")
@click.option(
    "--name",
    default="",
    help="The name of the template"
)
@click.option(
    "--description",
    default="",
    help="The description of the template"
)
def update(
    id,
    name,
    description
):
    """Update template with ID with the specified parameters"""
    print(
        templates.update(
            id,
            name,
            description
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
    """Subscribe to receive notifications about the template specified by ID"""
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
    templates.subscribe(
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
    """Delete subscription to the template with the specified by ID and email"""
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
    templates.unsubscribe(
        id,
        email
    )
