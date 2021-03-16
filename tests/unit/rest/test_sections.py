import pprint

import mockito
import pytest

from carrot_cli.rest import sections, request_handler


@pytest.fixture(autouse=True)
def unstub():
    yield
    mockito.unstub()


@pytest.fixture(
    params=[
        {
            "id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
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
                                    "print(message)",
                                ]
                            }
                        ]
                    },
                    "description": "This section will save Etheria",
                    "name": "Sword of Protection section",
                    "section_id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
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
    mockito.when(request_handler).find_by_id(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).find_by_id(
        "sections", request.param["id"]
    ).thenReturn(request.param["return"])
    return request.param


def test_find_by_id(find_by_id_data):
    result = sections.find_by_id(find_by_id_data["id"])
    assert result == find_by_id_data["return"]


@pytest.fixture(
    params=[
        {
            "params": [
                ("section_id", ""),
                ("name", "Queen of Bright Moon section"),
                ("description", ""),
                ("contents", ""),
                ("created_by", ""),
                ("created_before", ""),
                ("created_after", ""),
                ("sort", ""),
                ("limit", ""),
                ("offset", ""),
            ],
            "return": pprint.PrettyPrinter().pformat(
                [
                    {
                        "created_at": "2020-09-16T18:48:08.371563",
                        "created_by": "glimmer@example.com",
                        "contents": {
                            "cells":[
                                {
                                    "cell_type": "code",
                                    "execution_count": None,
                                    "metadata": {},
                                    "outputs": [],
                                    "source": [
                                        "print(message)",
                                    ]
                                }
                            ]
                        },
                        "description": "This section leads the Rebellion",
                        "name": "Queen of Bright Moon section",
                        "section_id": "bd132568-06fe-4b1a-9e96-47d4f36bf819",
                    }
                ]
            ),
        },
        {
            "params": [
                ("section_id", "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8"),
                ("name", ""),
                ("description", ""),
                ("contents", ""),
                ("created_by", ""),
                ("created_before", ""),
                ("created_after", ""),
                ("sort", ""),
                ("limit", ""),
                ("offset", ""),
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
    mockito.when(request_handler).find(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).find("sections", request.param["params"]).thenReturn(
        request.param["return"]
    )
    return request.param


def test_find(find_data):
    result = sections.find(
        find_data["params"][0][1],
        find_data["params"][1][1],
        find_data["params"][2][1],
        find_data["params"][3][1],
        find_data["params"][4][1],
        find_data["params"][5][1],
        find_data["params"][6][1],
        find_data["params"][7][1],
        find_data["params"][8][1],
        find_data["params"][9][1],
    )
    assert result == find_data["return"]


@pytest.fixture(
    params=[
        {
            "params": [
                ("name", "Horde Emperor section"),
                ("description", "This section rules the known universe"),
                (
                    "contents", 
                    {
                        "cells":[
                            {
                                "cell_type": "code",
                                "execution_count": None,
                                "metadata": {},
                                "outputs": [],
                                "source": [
                                    "print(message)",
                                ]
                            }
                        ]
                    }
                ),
                ("created_by", "hordeprime@example.com"),
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:08.371563",
                    "created_by": "hordeprime@example.com",
                    "contents": {},
                    "description": "This section rules the known universe",
                    "name": "Horde Emperor section",
                    "section_id": "bd132568-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "params": [
                ("name", "Horde Emperor section"),
                ("description", "This section rules the known universe"),
                ("contents", {}),
                ("created_by", "hordeprime@example.com"),
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "Server error",
                    "status": 500,
                    "detail": "Error while attempting to insert new section",
                }
            ),
        },
    ]
)
def create_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).create(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).create(
        "sections", request.param["params"]
    ).thenReturn(request.param["return"])
    return request.param


def test_create(create_data):
    result = sections.create(
        create_data["params"][0][1],
        create_data["params"][1][1],
        create_data["params"][2][1],
        create_data["params"][3][1],
    )
    assert result == create_data["return"]


@pytest.fixture(
    params=[
        {
            "id": "bd132568-06fe-4b1a-9e96-47d4f36bf819",
            "params": [
                ("name", "Catra section"),
                (
                    "description",
                    "This section is trying to learn to process anger better",
                ),
                (
                    "contents", 
                    {
                        "cells":[
                            {
                                "cell_type": "code",
                                "execution_count": None,
                                "metadata": {},
                                "outputs": [],
                                "source": [
                                    "print(message)",
                                ]
                            }
                        ]
                    }
                )
            ],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "created_at": "2020-09-16T18:48:08.371563",
                    "created_by": "catra@example.com",
                    "contents": {
                        "cells":[
                            {
                                "cell_type": "code",
                                "execution_count": None,
                                "metadata": {},
                                "outputs": [],
                                "source": [
                                    "print(message)",
                                ]
                            }
                        ]
                    },
                    "description": "This section is trying to learn to process anger better",
                    "name": "Catra section",
                    "section_id": "bd132568-06fe-4b1a-9e96-47d4f36bf819",
                }
            ),
        },
        {
            "id": "98536487-06fe-4b1a-9e96-47d4f36bf819",
            "params": [("name", "Angella section"), ("description", ""), ("contents", {})],
            "return": pprint.PrettyPrinter().pformat(
                {
                    "title": "Server error",
                    "status": 500,
                    "detail": "Error while attempting to update new section",
                }
            ),
        },
    ]
)
def update_data(request):
    # Set all requests to return None so only the one we expect will return a value
    mockito.when(request_handler).update(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).update(
        "sections", request.param["id"], request.param["params"]
    ).thenReturn(request.param["return"])
    return request.param


def test_update(update_data):
    result = sections.update(
        update_data["id"],
        update_data["params"][0][1],
        update_data["params"][1][1],
        update_data["params"][2][1],
    )
    assert result == update_data["return"]


@pytest.fixture(
    params=[
        {
            "id": "cd987859-06fe-4b1a-9e96-47d4f36bf819",
            "return": pprint.PrettyPrinter().pformat(
                {
                    "message": "Successfully deleted 1 row"
                }
            ),
        },
        {
            "id": "3d1bfbab-d9ec-46c7-aa8e-9c1d1808f2b8",
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
    mockito.when(request_handler).delete(...).thenReturn(None)
    # Mock up request response
    mockito.when(request_handler).delete(
        "sections", request.param["id"]
    ).thenReturn(request.param["return"])
    return request.param


def test_delete(delete_data):
    result = sections.delete(delete_data["id"])
    assert result == delete_data["return"]
