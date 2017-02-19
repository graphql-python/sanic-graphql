import pytest
import json

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from aiohttp.helpers import FormData


from .util import app, client, url_string, create_app



def response_json(response):
    return json.loads(response.body.decode())


j = lambda **kwargs: json.dumps(kwargs)
jl = lambda **kwargs: json.dumps([kwargs])


def test_allows_get_with_query_param(app, client):
    response = client.get(app, uri=url_string(query='{test}'))

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello World"}
    }


def test_allows_get_with_variable_values(app, client):
    response = client.get(app, uri=url_string(
        query='query helloWho($who: String){ test(who: $who) }',
        variables=json.dumps({'who': "Dolly"})
    ))

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello Dolly"}
    }


def test_allows_get_with_operation_name(app, client):
    response = client.get(app, uri=url_string(
        query='''
        query helloYou { test(who: "You"), ...shared }
        query helloWorld { test(who: "World"), ...shared }
        query helloDolly { test(who: "Dolly"), ...shared }
        fragment shared on QueryRoot {
          shared: test(who: "Everyone")
        }
        ''',
        operationName='helloWorld'
    ))

    assert response.status == 200
    assert response_json(response) == {
        'data': {
            'test': 'Hello World',
            'shared': 'Hello Everyone'
        }
    }


def test_reports_validation_errors(app, client):
    response = client.get(app, uri=url_string(
        query='{ test, unknownOne, unknownTwo }'
    ))

    assert response.status == 400
    assert response_json(response) == {
        'errors': [
            {
                'message': 'Cannot query field "unknownOne" on type "QueryRoot".',
                'locations': [{'line': 1, 'column': 9}]
            },
            {
                'message': 'Cannot query field "unknownTwo" on type "QueryRoot".',
                'locations': [{'line': 1, 'column': 21}]
            }
        ]
    }


def test_errors_when_missing_operation_name(app, client):
    response = client.get(app, uri=url_string(
        query='''
        query TestQuery { test }
        mutation TestMutation { writeTest { test } }
        '''
    ))

    assert response.status == 400
    assert response_json(response) == {
        'errors': [
            {
                'message': 'Must provide operation name if query contains multiple operations.'
            }
        ]
    }


def test_errors_when_sending_a_mutation_via_get(app, client):
    response = client.get(app, uri=url_string(
        query='''
        mutation TestMutation { writeTest { test } }
        '''
    ))
    assert response.status == 405
    assert response_json(response) == {
        'errors': [
            {
                'message': 'Can only perform a mutation operation from a POST request.'
            }
        ]
    }


def test_errors_when_selecting_a_mutation_within_a_get(app, client):
    response = client.get(app, uri=url_string(
        query='''
        query TestQuery { test }
        mutation TestMutation { writeTest { test } }
        ''',
        operationName='TestMutation'
    ))

    assert response.status == 405
    assert response_json(response) == {
        'errors': [
            {
                'message': 'Can only perform a mutation operation from a POST request.'
            }
        ]
    }


def test_allows_mutation_to_exist_within_a_get(app, client):
    response = client.get(app, uri=url_string(
        query='''
        query TestQuery { test }
        mutation TestMutation { writeTest { test } }
        ''',
        operationName='TestQuery'
    ))

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello World"}
    }


def test_allows_post_with_json_encoding(app, client):
    response = client.post(app, uri=url_string(), data=j(query='{test}'), headers={'content-type': 'application/json'})

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello World"}
    }


def test_allows_sending_a_mutation_via_post(app, client):
    response = client.post(app, uri=url_string(), data=j(query='mutation TestMutation { writeTest { test } }'), headers={'content-type': 'application/json'})

    assert response.status == 200
    assert response_json(response) == {
        'data': {'writeTest': {'test': 'Hello World'}}
    }


def test_allows_post_with_url_encoding(app, client):
    data = FormData()
    data.add_field('query', '{test}')
    response = client.post(app, uri=url_string(), data=data('utf-8'), headers={'content-type': data.content_type})

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello World"}
    }


def test_supports_post_json_query_with_string_variables(app, client):
    response = client.post(app, uri=url_string(), data=j(
        query='query helloWho($who: String){ test(who: $who) }',
        variables=json.dumps({'who': "Dolly"})
    ), headers={'content-type': 'application/json'})

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello Dolly"}
    }


def test_supports_post_json_query_with_json_variables(app, client):
    response = client.post(app, uri=url_string(), data=j(
        query='query helloWho($who: String){ test(who: $who) }',
        variables={'who': "Dolly"}
    ), headers={'content-type': 'application/json'})

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello Dolly"}
    }


def test_supports_post_url_encoded_query_with_string_variables(app, client):
    response = client.post(app, uri=url_string(), data=urlencode(dict(
        query='query helloWho($who: String){ test(who: $who) }',
        variables=json.dumps({'who': "Dolly"})
    )), headers={'content-type': 'application/x-www-form-urlencoded'})

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello Dolly"}
    }


def test_supports_post_json_quey_with_get_variable_values(app, client):
    response = client.post(app, uri=url_string(
        variables=json.dumps({'who': "Dolly"})
    ), data=j(
        query='query helloWho($who: String){ test(who: $who) }',
    ), headers={'content-type': 'application/json'})

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello Dolly"}
    }


def test_post_url_encoded_query_with_get_variable_values(app, client):
    response = client.post(app, uri=url_string(
        variables=json.dumps({'who': "Dolly"})
    ), data=urlencode(dict(
        query='query helloWho($who: String){ test(who: $who) }',
    )), headers={'content-type': 'application/x-www-form-urlencoded'})

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello Dolly"}
    }


def test_supports_post_raw_text_query_with_get_variable_values(app, client):
    response = client.post(app, uri=url_string(
        variables=json.dumps({'who': "Dolly"})
    ),
        data='query helloWho($who: String){ test(who: $who) }',
        headers={'content-type': 'application/graphql'}
    )

    assert response.status == 200
    assert response_json(response) == {
        'data': {'test': "Hello Dolly"}
    }


def test_allows_post_with_operation_name(app, client):
    response = client.post(app, uri=url_string(), data=j(
        query='''
        query helloYou { test(who: "You"), ...shared }
        query helloWorld { test(who: "World"), ...shared }
        query helloDolly { test(who: "Dolly"), ...shared }
        fragment shared on QueryRoot {
          shared: test(who: "Everyone")
        }
        ''',
        operationName='helloWorld'
    ), headers={'content-type': 'application/json'})

    assert response.status == 200
    assert response_json(response) == {
        'data': {
            'test': 'Hello World',
            'shared': 'Hello Everyone'
        }
    }


def test_allows_post_with_get_operation_name(app, client):
    response = client.post(app, uri=url_string(
        operationName='helloWorld'
    ), data='''
    query helloYou { test(who: "You"), ...shared }
    query helloWorld { test(who: "World"), ...shared }
    query helloDolly { test(who: "Dolly"), ...shared }
    fragment shared on QueryRoot {
      shared: test(who: "Everyone")
    }
    ''',
        headers={'content-type': 'application/graphql'})

    assert response.status == 200
    assert response_json(response) == {
        'data': {
            'test': 'Hello World',
            'shared': 'Hello Everyone'
        }
    }


@pytest.mark.parametrize('app', [create_app(pretty=True)])
def test_supports_pretty_printing(app, client):
    response = client.get(app, uri=url_string(query='{test}'))

    assert response.body.decode() == (
        '{\n'
        '  "data": {\n'
        '    "test": "Hello World"\n'
        '  }\n'
        '}'
    )


@pytest.mark.parametrize('app', [create_app(pretty=False)])
def test_not_pretty_by_default(app, client):
    response = client.get(app, url_string(query='{test}'))

    assert response.body.decode() == (
        '{"data":{"test":"Hello World"}}'
    )


def test_supports_pretty_printing_by_request(app, client):
    response = client.get(app, uri=url_string(query='{test}', pretty='1'))

    assert response.body.decode() == (
        '{\n'
        '  "data": {\n'
        '    "test": "Hello World"\n'
        '  }\n'
        '}'
    )


def test_handles_field_errors_caught_by_graphql(app, client):
    response = client.get(app, uri=url_string(query='{thrower}'))
    assert response.status == 200
    assert response_json(response) == {
        'data': None,
        'errors': [{'locations': [{'column': 2, 'line': 1}], 'message': 'Throws!'}]
    }


def test_handles_syntax_errors_caught_by_graphql(app, client):
    response = client.get(app, uri=url_string(query='syntaxerror'))
    assert response.status == 400
    assert response_json(response) == {
        'errors': [{'locations': [{'column': 1, 'line': 1}],
                    'message': 'Syntax Error GraphQL request (1:1) '
                               'Unexpected Name "syntaxerror"\n\n1: syntaxerror\n   ^\n'}]
    }


def test_handles_errors_caused_by_a_lack_of_query(app, client):
    response = client.get(app, uri=url_string())

    assert response.status == 400
    assert response_json(response) == {
        'errors': [{'message': 'Must provide query string.'}]
    }


def test_handles_invalid_json_bodies(app, client):
    response = client.post(app, uri=url_string(), data='[]', headers={'content-type': 'application/json'})

    assert response.status == 400
    assert response_json(response) == {
        'errors': [{'message': 'POST body sent invalid JSON.'}]
    }


def test_handles_incomplete_json_bodies(app, client):
    response = client.post(app, uri=url_string(), data='{"query":', headers={'content-type': 'application/json'})

    assert response.status == 400
    assert response_json(response) == {
        'errors': [{'message': 'POST body sent invalid JSON.'}]
    }


def test_handles_plain_post_text(app, client):
    response = client.post(app, uri=url_string(
        variables=json.dumps({'who': "Dolly"})
    ),
        data='query helloWho($who: String){ test(who: $who) }',
        headers={'content-type': 'text/plain'}
    )
    assert response.status == 400
    assert response_json(response) == {
        'errors': [{'message': 'Must provide query string.'}]
    }


def test_handles_poorly_formed_variables(app, client):
    response = client.get(app, uri=url_string(
        query='query helloWho($who: String){ test(who: $who) }',
        variables='who:You'
    ))
    assert response.status == 400
    assert response_json(response) == {
        'errors': [{'message': 'Variables are invalid JSON.'}]
    }


def test_handles_unsupported_http_methods(app, client):
    response = client.put(app, uri=url_string(query='{test}'))
    assert response.status == 405
    assert response.headers['Allow'] in ['GET, POST', 'HEAD, GET, POST, OPTIONS']
    assert response_json(response) == {
        'errors': [{'message': 'GraphQL only supports GET and POST requests.'}]
    }


def test_passes_request_into_request_context(app, client):
    response = client.get(app, uri=url_string(query='{request}', q='testing'))

    assert response.status == 200
    assert response_json(response) == {
        'data': {
            'request': 'testing'
        }
    }


@pytest.mark.parametrize('app', [create_app(context="CUSTOM CONTEXT")])
def test_supports_pretty_printing(app, client):
    response = client.get(app, uri=url_string(query='{context}'))


    assert response.status == 200
    assert response_json(response) == {
        'data': {
            'context': 'CUSTOM CONTEXT'
        }
    }


def test_post_multipart_data(app, client):
    query = 'mutation TestMutation { writeTest { test } }'

    data = ('------sanicgraphql\r\n' +
            'Content-Disposition: form-data; name="query"\r\n' +
            '\r\n' +
            query + '\r\n' +
            '------sanicgraphql--\r\n' + 
            'Content-Type: text/plain; charset=utf-8\r\n' + 
            'Content-Disposition: form-data; name="file"; filename="text1.txt"; filename*=utf-8\'\'text1.txt\r\n' + 
            '\r\n' +
            '\r\n' +
            '------sanicgraphql--\r\n'
    )

    response = client.post(
        app,
        uri=url_string(),
        data=data,
        headers={'content-type': 'multipart/form-data; boundary=----sanicgraphql'}
    )

    assert response.status == 200
    assert response_json(response) == {'data': {u'writeTest': {u'test': u'Hello World'}}}


@pytest.mark.parametrize('app', [create_app(batch=True)])
def test_batch_allows_post_with_json_encoding(app, client):
    response = client.post(
        app,
        uri=url_string(),
        data=jl(id=1, query='{test}'),
        headers={'content-type': 'application/json'}
    )

    assert response.status == 200
    assert response_json(response) == [{
        'id': 1,
        'payload': { 'data': {'test': "Hello World"} },
        'status': 200,
    }]


@pytest.mark.parametrize('app', [create_app(batch=True)])
def test_batch_supports_post_json_query_with_json_variables(app, client):
    response = client.post(
        app,
        uri=url_string(),
        data=jl(
            id=1,
            query='query helloWho($who: String){ test(who: $who) }',
            variables={'who': "Dolly"}
        ),
        headers={'content-type': 'application/json'}
    )

    assert response.status == 200
    assert response_json(response) == [{
        'id': 1,
        'payload': { 'data': {'test': "Hello Dolly"} },
        'status': 200,
    }]
 
          
@pytest.mark.parametrize('app', [create_app(batch=True)])
def test_batch_allows_post_with_operation_name(app, client):
    response = client.post(
        app,
        uri=url_string(),
        data=jl(
            id=1,
            query='''
            query helloYou { test(who: "You"), ...shared }
            query helloWorld { test(who: "World"), ...shared }
            query helloDolly { test(who: "Dolly"), ...shared }
            fragment shared on QueryRoot {
              shared: test(who: "Everyone")
            }
            ''',
            operationName='helloWorld'
        ),
        headers={'content-type': 'application/json'}
    )

    assert response.status == 200
    assert response_json(response) == [{
        'id': 1,
        'payload': {
            'data': {
                'test': 'Hello World',
                'shared': 'Hello Everyone'
            }
        },
        'status': 200,
    }]
