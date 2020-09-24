import logging
import click

from ..rest import subscriptions

LOGGER = logging.getLogger(__name__)


@click.group(name="subscription")
def main():
    """Commands for searching subscriptions"""

@main.command(name="find_by_id")
@click.argument("id")
def find_by_id(id):
    """Retrieve a subscription by its ID"""
    print(subscriptions.find_by_id(id))

@main.command(name="find")
@click.option(
    "--subscription_id",
    default="",
    help="The subscription's ID, a version 4 UUID"
)
@click.option(
    "--entity_type",
    default="",
    help="The type of the entity subscribed to (pipeline, template, or test)"
)
@click.option(
    "--entity_id",
    default="",
    help="The entity's ID, a version 4 UUID"
)
@click.option(
    "--created_before",
    default="",
    help="Upper bound for subscription's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--created_after",
    default="",
    help="Lower bound for subscription's created_at value, in the format YYYY-MM-DDThh:mm:ss.ssssss"
)
@click.option(
    "--email",
    default="",
    help="Email of the subscriber, case sensitive"
)
@click.option(
    "--sort",
    default="",
    help="A comma-separated list of sort keys, enclosed in asc() for ascending or desc() for "
        "descending.  Ex. asc(entity_type),desc(entity_id)"
)
@click.option(
    "--limit",
    default=20,
    show_default=True,
    help="The maximum number of subscription records to return"
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
    subscription_id,
    entity_type,
    entity_id,
    created_before,
    created_after,
    email,
    sort,
    limit,
    offset
):
    """Retrieve subscriptions filtered to match the specified parameters"""
    print(
        subscriptions.find(
            subscription_id,
            entity_type,
            entity_id,
            created_before,
            created_after,
            email,
            sort,
            limit,
            offset
    ))
