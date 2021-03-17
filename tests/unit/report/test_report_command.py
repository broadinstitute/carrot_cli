import pprint

import mockito
import pytest
from click.testing import CliRunner

from carrot_cli.__main__ import main_entry as carrot
from carrot_cli.config import manager as config
from carrot_cli.rest import reports, report_sections


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
            "args": ["report", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "description": "This report will save Etheria",
                    "metadata": {
                        "metadata": {
                            "language_info": {
                                "codemirror_mode": {
                                    "name": "ipython",
                                    "version": 3
                                },
                                "file_extension": ".py",
                                "mimetype": "text/x-python",
                                "name": "python",
                                "nbconvert_exporter": "python",
                                "pygments_lexer": "ipython3",
                                "version": "3.8.5-final"
                            },
                            "orig_nbformat": 2,
                            "kernelspec": {
                                "name": "python3",
                                "display_name": "Python 3.8.5 64-bit",
                                "metadata": {
                                    "interpreter": {
                                        "hash": "1ee38ef4a5a9feb55287fd749643f13d043cb0a7addaab2a9c224cbe137c0062"
                                    }
                                }
                            }
                        },
                        "nbformat": 4,
                        "nbformat_minor": 2
                    },
                    "name": "Sword of Protection report",
                    "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": ["report", "find_by_id", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No report found",
                    "status": 404,
                    "detail": "No report found with the specified ID",
                }
            ),
        },
    ]
)
def find_by_id_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(reports).find_by_id(...).thenReturn(None)
    # Mock up request response
    mockito.when(reports).find_by_id(request.param["args"][2]).thenReturn(
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
                "report",
                "find",
                "--report_id",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--name",
                "Sword of Protection report",
                "--description",
                "This report will save Etheria",
                "--metadata",
                "tests/data/mock_report_metadata.json",
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
                "Sword of Protection report",
                "This report will save Etheria",
                {
                    "metadata": {
                        "language_info": {
                            "codemirror_mode": {
                                "name": "ipython",
                                "version": 3
                            },
                            "file_extension": ".py",
                            "mimetype": "text/x-python",
                            "name": "python",
                            "nbconvert_exporter": "python",
                            "pygments_lexer": "ipython3",
                            "version": "3.8.5-final"
                        },
                        "orig_nbformat": 2,
                        "kernelspec": {
                            "name": "python3",
                            "display_name": "Python 3.8.5 64-bit",
                            "metadata": {
                                "interpreter": {
                                    "hash": "1ee38ef4a5a9feb55287fd749643f13d043cb0a7addaab2a9c224cbe137c0062"
                                }
                            }
                        }
                    },
                    "nbformat": 4,
                    "nbformat_minor": 2
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
                    "description": "This report will save Etheria",
                    "metadata": {
                        "metadata": {
                            "language_info": {
                                "codemirror_mode": {
                                    "name": "ipython",
                                    "version": 3
                                },
                                "file_extension": ".py",
                                "mimetype": "text/x-python",
                                "name": "python",
                                "nbconvert_exporter": "python",
                                "pygments_lexer": "ipython3",
                                "version": "3.8.5-final"
                            },
                            "orig_nbformat": 2,
                            "kernelspec": {
                                "name": "python3",
                                "display_name": "Python 3.8.5 64-bit",
                                "metadata": {
                                    "interpreter": {
                                        "hash": "1ee38ef4a5a9feb55287fd749643f13d043cb0a7addaab2a9c224cbe137c0062"
                                    }
                                }
                            }
                        },
                        "nbformat": 4,
                        "nbformat_minor": 2
                    },
                    "name": "Sword of Protection report",
                    "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": [
                "report",
                "find",
                "--report_id",
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
                    "title": "No reports found",
                    "status": 404,
                    "detail": "No reports found with the specified parameters",
                }
            ),
        },
    ]
)
def find_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(reports).find(...).thenReturn(None)
    # Mock up request response
    mockito.when(reports).find(
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
                "report",
                "create",
                "--name",
                "Sword of Protection report",
                "--description",
                "This report will save Etheria",
                "--created_by",
                "adora@example.com",
            ],
            "params": [
                "Sword of Protection report",
                "This report will save Etheria",
                "adora@example.com",
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "description": "This report will save Etheria",
                    "metadata": {
                        "metadata": {
                            "language_info": {
                                "codemirror_mode": {
                                    "name": "ipython",
                                    "version": 3
                                },
                                "file_extension": ".py",
                                "mimetype": "text/x-python",
                                "name": "python",
                                "nbconvert_exporter": "python",
                                "pygments_lexer": "ipython3",
                                "version": "3.8.5-final"
                            },
                            "orig_nbformat": 2,
                            "kernelspec": {
                                "name": "python3",
                                "display_name": "Python 3.8.5 64-bit",
                                "metadata": {
                                    "interpreter": {
                                        "hash": "1ee38ef4a5a9feb55287fd749643f13d043cb0a7addaab2a9c224cbe137c0062"
                                    }
                                }
                            }
                        },
                        "nbformat": 4,
                        "nbformat_minor": 2
                    },
                    "name": "Sword of Protection report",
                    "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": [
                "report",
                "create",
                "--name",
                "Sword of Protection report",
                "--description",
                "This report will save Etheria",
            ],
            "params": [],
            "return": "No email config variable set.  If a value is not specified for --created by, "
                "there must be a value set for email."
        },
        {
            "args": ["report", "create"],
            "params": [],
            "return": "Usage: carrot_cli report create [OPTIONS]\n"
            "Try 'carrot_cli report create --help' for help.\n"
            "\n"
            "Error: Missing option '--name'.",
        },
    ]
)
def create_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(reports).create(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(reports).create(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
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
                "report",
                "update",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--description",
                "This new report replaced the broken one",
                "--name",
                "New Sword of Protection report",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "New Sword of Protection report",
                "This new report replaced the broken one",
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:06.371563",
                    "created_by": "adora@example.com",
                    "description": "This new report replaced the broken one",
                    "name": "New Sword of Protection report",
                    "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "args": ["report", "update"],
            "params": [],
            "return": "Usage: carrot_cli report update [OPTIONS] ID\n"
            "Try 'carrot_cli report update --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def update_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(reports).update(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(reports).update(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
        ).thenReturn(request.param["return"])
    return request.param


def test_update(update_data):
    runner = CliRunner()
    result = runner.invoke(carrot, update_data["args"])
    assert result.output == update_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": ["report", "delete", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "message": "Successfully deleted 1 row"
                }
            ),
        },
        {
            "args": ["report", "delete", "cd987859-06fe-4b1a-9e96-47d4f36bf819"],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "No report found",
                    "status": 404,
                    "detail": "No report found with the specified ID",
                }
            ),
        },
    ]
)
def delete_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(reports).delete(...).thenReturn(None)
    # Mock up request response
    mockito.when(reports).delete(request.param["args"][2]).thenReturn(
        request.param["return"]
    )
    return request.param


def test_delete(delete_data):
    runner = CliRunner()
    result = runner.invoke(carrot, delete_data["args"])
    assert result.output == delete_data["return"] + "\n"

@pytest.fixture(
    params=[
        {
            "args": [
                "report",
                "map_to_section",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "out_horde_tanks",
                "1",
                "--created_by",
                "adora@example.com",
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "out_horde_tanks",
                "1",
                "adora@example.com",
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "name": "out_horde_tanks",
                    "position": "1",
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "rogelio@example.com",
                }
            ),
        },
        {
            "args": [
                "report",
                "map_to_section",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "out_horde_tanks",
                "1"
            ],
            "params": [],
            "return": "No email config variable set.  If a value is not specified for --created by, "
                "there must be a value set for email."
        },
        {
            "args": ["report", "map_to_section"],
            "params": [],
            "return": "Usage: carrot_cli report map_to_section [OPTIONS] ID SECTION_ID NAME POSITION\n"
            "Try 'carrot_cli report map_to_section --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def map_to_section_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(report_sections).create_map(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(report_sections).create_map(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
            request.param["params"][3],
            request.param["params"][4],
        ).thenReturn(request.param["return"])
    return request.param


def test_map_to_section(map_to_section_data):
    runner = CliRunner()
    result = runner.invoke(carrot, map_to_section_data["args"])
    assert result.output == map_to_section_data["return"] + "\n"


@pytest.fixture(
    params=[
        {
            "args": [
                "report",
                "find_section_map_by_ids_and_name",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "section_name"
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "section_name"
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                    "section_id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                    "name": "section_name",
                    "position": "1",
                    "created_at": "2020-09-24T19:07:59.311462",
                    "created_by": "rogelio@example.com",
                }
            ),
        },
        {
            "args": ["report", "find_section_map_by_ids_and_name"],
            "params": [],
            "return": "Usage: carrot_cli report find_section_map_by_ids_and_name [OPTIONS] ID\n"
            "                                                          SECTION_ID NAME\n"
            "Try 'carrot_cli report find_section_map_by_ids_and_name --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def find_section_map_by_ids_and_name_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(report_sections).find_map_by_ids_and_name(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(report_sections).find_map_by_ids_and_name(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
        ).thenReturn(request.param["return"])
    return request.param


def test_find_section_map_by_ids_and_name(find_section_map_by_ids_and_name_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_section_map_by_ids_and_name_data["args"])
    assert result.output == find_section_map_by_ids_and_name_data["return"] + "\n"

@pytest.fixture(
    params=[
        {
            "args": [
                "report",
                "delete_section_map_by_ids_and_name",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "section_name"
            ],
            "params": [
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "section_name"
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "message": "Successfully deleted 1 row"
                }
            ),
        },
        {
            "args": ["report", "delete_section_map_by_ids_and_name"],
            "params": [],
            "return": "Usage: carrot_cli report delete_section_map_by_ids_and_name [OPTIONS] ID\n"
            "                                                            SECTION_ID NAME\n"
            "Try 'carrot_cli report delete_section_map_by_ids_and_name --help' for help.\n"
            "\n"
            "Error: Missing argument 'ID'.",
        },
    ]
)
def delete_section_map_by_ids_and_name_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(report_sections).delete_map_by_ids_and_name(...).thenReturn(None)
    # Mock up request response only if we expect it to get that far
    if len(request.param["params"]) > 0:
        mockito.when(report_sections).delete_map_by_ids_and_name(
            request.param["params"][0],
            request.param["params"][1],
            request.param["params"][2],
        ).thenReturn(request.param["return"])
    return request.param


def test_delete_section_map_by_ids_and_name(delete_section_map_by_ids_and_name_data):
    runner = CliRunner()
    result = runner.invoke(carrot, delete_section_map_by_ids_and_name_data["args"])
    assert result.output == delete_section_map_by_ids_and_name_data["return"] + "\n"

@pytest.fixture(
    params=[
        {
            "args": [
                "report",
                "find_section_maps",
                "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                "--section_id",
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "--name",
                "sword_of_protection",
                "--position",
                "1",
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
                "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                "sword_of_protection",
                "1",
                "2020-10-00T00:00:00.000000",
                "2020-09-00T00:00:00.000000",
                "adora@example.com",
                "asc(name)",
                1,
                0,
            ],
            "return": pprint.PrettyPrinter().pformat(
                [
                    {
                        "report_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                        "section_id": "4d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
                        "name": "sword_of_protection_key",
                        "position": "1",
                        "created_at": "2020-09-24T19:07:59.311462",
                        "created_by": "adora@example.com",
                    }
                ]
            ),
        },
        {
            "args": [
                "report",
                "find_section_maps",
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
                    "title": "No report_sections found",
                    "status": 404,
                    "detail": "No report_sections found with the specified parameters",
                }
            ),
        },
    ]
)
def find_section_maps_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(report_sections).find_maps(...).thenReturn(None)
    # Mock up request response
    mockito.when(report_sections).find_maps(
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


def test_find_section_maps(find_section_maps_data):
    runner = CliRunner()
    result = runner.invoke(carrot, find_section_maps_data["args"])
    assert result.output == find_section_maps_data["return"] + "\n"
