import pprint

import mockito
import pytest
from click.testing import CliRunner

from carrot_cli.__main__ import main_entry as carrot
from carrot_cli.config import manager as config
from carrot_cli.rest import sections


@pytest.fixture(autouse=True)
def unstub():
    yield
    mockito.unstub()

@pytest.fixture(autouse=True)
def no_email():
    mockito.when(config).load_var_no_error("email").thenReturn(None)
   
@pytest.fixture(
    params=[
        {
            "args": ["section", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "contents": {
                        "cells":[
                            {
                                "cell_type": "code",
                                "execution_count": None,
                                "metadata": {},
                                "outputs": [],
                                "source": [
                                    "print(message)"
                                ]
                            }
                        ]
                    },
                    "description": "This section will save Etheria",
                    "name": "Sword of Protection Section",
                    "section_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": ["section", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No section found",
                    "status": 404,
                    "detail": "No section found with the specified ID",
                }
            ),
        },
    ]
)
def find_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(sections).find_by_id(...).thenReturn(None)
    # Mock up request response
    mockito.when(sections).find_by_id(request.param["args"][2]).thenReturn(
        request.param["return"]
    )
    return request.param


def test_find_by_id(find_by_id_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_by_id_data["args"])
    assert result.output == find_by_id_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "section",
                "find",
                "--section_id",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--name",
                "Sword of Protection Section",
                "--description",
                "This section will save Etheria",
                "--contents",
                "tests/data/mock_section_contents.json",
                "--created_by",
                "adora@example.com",
                "--created_before",
                "2020-10-00T00:00:00.000000",
                "--created_after",
                "2020-09-00T00:00:00.000000",
                "--sort",
                "asc(name)",
                "--limit",
                1,
                "--offset",
                0,
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "Sword of Protection Section",
                "This section will save Etheria",
                {
                    "cells":[
                        {
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {},
                            "outputs": [],
                            "source": [
                                "print(message)"
                            ]
                        }
                    ]
                },
                "adora@example.com",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "asc(name)",
                1,
                0,
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "contents": {
                        "cells":[
                            {
                                "cell_type": "code",
                                "execution_count": None,
                                "metadata": {},
                                "outputs": [],
                                "source": [
                                    "print(message)"
                                ]
                            }
                        ]
                    },
                    "description": "This section will save Etheria",
                    "name": "Sword of Protection Section",
                    "section_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": [
                "section",
                "find",
                "--section_id",
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
            ],
            "params": [
                "986325ba-06fe-4b1a-9e96-47d4f36bf819",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                20,
                0,
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No sections found",
                    "status": 404,
                    "detail": "No sections found with the specified parameters",
                }
            ),
        },
    ]
)
def find_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(sections).find(...).thenReturn(None)
    # Mock up request response
    mockito.when(sections).find(
        request.param["params"][0],
        request.param["params"][1],
        request.param["params"][2],
        request.param["params"][3],
        request.param["params"][4],
        request.param["params"][5],
        request.param["params"][6],
        request.param["params"][7],
        request.param["params"][8],
        request.param["params"][9],
    ).thenReturn(request.param["return"])
    return request.param


def test_find(find_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_data["args"])
    assert result.output == find_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "section",
                "create",
                "--name",
                "Sword of Protection Section",
                "--description",
                "This section will save Etheria",
                "--contents",
                "tests/data/mock_section_contents.json",
                "--created_by",
                "adora@example.com",
            ],
            "params": [
                "Sword of Protection Section",
                "This section will save Etheria",
                {
                    "cells":[
                        {
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {},
                            "outputs": [],
                            "source": [
                                "print(message)"
                            ]
                        }
                    ]
                },
                "adora@example.com",
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "contents": {
                        "cells":[
                            {
                                "cell_type": "code",
                                "execution_count": None,
                                "metadata": {},
                                "outputs": [],
                                "source": [
                                    "print(message)"
                                ]
                            }
                        ]
                    },
                    "description": "This section will save Etheria",
                    "name": "Sword of Protection Section",
                    "section_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": [
                "section",
                "create",
                "--name",
                "Sword of Protection Section",
                "--description",
                "This section will save Etheria",
                "--contents",
                "tests/data/mock_section_contents.json",
            ],
            "params": [],
            "return": "No email config variable set.  If a value is not specified for --created by, "
                "there must be a value set for email."
        },
        {
            "args": ["section", "create"],
            "params": [],
            "return": "Usage: carrot_cli section create [OPTIONS]\n"
            "Try 'carrot_cli section create --help' for help.\n"
            "\n"
            "Error: Missing option '--name'.",
        },
    ]
)
def create_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(sections).create(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(sections).create(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
            request.param["params"][3],
        ).thenReturn(request.param["return"])
    return request.param


def test_create(create_data):
    runner = CliRunner()
    result = runner.invoke(carrot, create_data["args"])
    assert result.output == create_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "section",
                "update",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--description",
                "This new section replaced the broken one",
                "--name",
                "New Sword of Protection Section",
                "--contents",
                "tests/data/mock_section_contents.json",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "New Sword of Protection Section",
                "This new section replaced the broken one",
                {
                    "cells":[
                        {
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {},
                            "outputs": [],
                            "source": [
                                "print(message)"
                            ]
                        }
                    ]
                }
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "contents": {
                        "cells":[
                            {
                                "cell_type": "code",
                                "execution_count": None,
                                "metadata": {},
                                "outputs": [],
                                "source": [
                                    "print(message)"
                                ]
                            }
                        ]
                    },
                    "description": "This new section replaced the broken one",
                    "name": "New Sword of Protection Section",
                    "section_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": ["section", "update"],
            "params": [],
            "return": "Usage: carrot_cli section update [OPTIONS] ID\n"
            "Try 'carrot_cli section update --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def update_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(sections).update(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(sections).update(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
            request.param["params"][3],
        ).thenReturn(request.param["return"])
    return request.param


def test_update(update_data):
    runner = CliRunner()
    result = runner.invoke(carrot, update_data["args"])
    assert result.output == update_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": ["section", "delete", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "message": "Successfully deleted 1 row"
                }
            ),
        },
        {
            "args": ["section", "delete", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No section found",
                    "status": 404,
                    "detail": "No section found with the specified ID",
                }
            ),
        },
    ]
)
def delete_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(sections).delete(...).thenReturn(None)
    # Mock up request response
    mockito.when(sections).delete(request.param["args"][2]).thenReturn(
        request.param["return"]
    )
    return request.param


def test_delete(delete_data):
    runner = CliRunner()
    result = runner.invoke(carrot, delete_data["args"])
    assert result.output == delete_data["return"] + "\n"
