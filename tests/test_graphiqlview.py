import pytest
from jinja2 import Environment

from .app import create_app, url_string
from .schema import AsyncSchema


@pytest.fixture
def pretty_response():
    return (
        "{\n"
        '  "data": {\n'
        '    "test": "Hello World"\n'
        "  }\n"
        "}".replace('"', '\\"').replace("\n", "\\n")
    )


@pytest.mark.parametrize("app", [create_app(graphiql=True)])
def test_graphiql_is_enabled(app):
    _, response = app.client.get(
        uri=url_string(query="{test}"), headers={"Accept": "text/html"}
    )
    assert response.status == 200


@pytest.mark.parametrize("app", [create_app(graphiql=True)])
def test_graphiql_simple_renderer(app, pretty_response):
    _, response = app.client.get(
        uri=url_string(query="{test}"), headers={"Accept": "text/html"}
    )
    assert response.status == 200
    assert pretty_response in response.body.decode("utf-8")


@pytest.mark.parametrize("app", [create_app(graphiql=True, jinja_env=Environment())])
def test_graphiql_jinja_renderer(app, pretty_response):
    _, response = app.client.get(
        uri=url_string(query="{test}"), headers={"Accept": "text/html"}
    )
    assert response.status == 200
    assert pretty_response in response.body.decode("utf-8")


@pytest.mark.parametrize(
    "app", [create_app(graphiql=True, jinja_env=Environment(enable_async=True))]
)
def test_graphiql_jinja_async_renderer(app, pretty_response):
    _, response = app.client.get(
        uri=url_string(query="{test}"), headers={"Accept": "text/html"}
    )
    assert response.status == 200
    assert pretty_response in response.body.decode("utf-8")


@pytest.mark.parametrize("app", [create_app(graphiql=True)])
def test_graphiql_html_is_not_accepted(app):
    _, response = app.client.get(
        uri=url_string(), headers={"Accept": "application/json"}
    )
    assert response.status == 400


@pytest.mark.parametrize(
    "app", [create_app(graphiql=True, schema=AsyncSchema, enable_async=True)]
)
def test_graphiql_asyncio_schema(app):
    query = "{a,b,c}"
    _, response = app.client.get(
        uri=url_string(query=query), headers={"Accept": "text/html"}
    )

    expected_response = (
        (
            "{\n"
            '  "data": {\n'
            '    "a": "hey",\n'
            '    "b": "hey2",\n'
            '    "c": "hey3"\n'
            "  }\n"
            "}"
        )
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )

    assert response.status == 200
    assert expected_response in response.body.decode("utf-8")
