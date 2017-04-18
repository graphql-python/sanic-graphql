from functools import partial
from cgi import parse_header


from promise import Promise
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView

from graphql.type.schema import GraphQLSchema
from graphql.execution.executors.asyncio import AsyncioExecutor
from graphql_server import (HttpQueryError, default_format_error,
                            encode_execution_results, json_encode,
                            load_json_body, run_http_query)

from .render_graphiql import render_graphiql


class GraphQLView(HTTPMethodView):
    schema = None
    executor = None
    root_value = None
    context = None
    pretty = False
    graphiql = False
    graphiql_version = None
    graphiql_template = None
    middleware = None
    batch = False
    jinja_env = None
    max_age = 86400

    _enable_async = True

    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def __init__(self, **kwargs):
        super(GraphQLView, self).__init__()
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self._enable_async = self._enable_async and isinstance(self.executor, AsyncioExecutor)
        assert isinstance(self.schema, GraphQLSchema), 'A Schema is required to be provided to GraphQLView.'

    # noinspection PyUnusedLocal
    def get_root_value(self, request):
        return self.root_value

    def get_context(self, request):
        context = self.context or {}
        if isinstance(context, dict) and 'request' not in context:
            context.update({'request': request})
        return context

    def get_middleware(self, request):
        return self.middleware

    def get_executor(self, request):
        return self.executor

    def render_graphiql(self, params, result):
        return render_graphiql(
            jinja_env=self.jinja_env,
            params=params,
            result=result,
            graphiql_version=self.graphiql_version,
            graphiql_template=self.graphiql_template,
        )

    format_error = staticmethod(default_format_error)
    encode = staticmethod(json_encode)

    async def dispatch_request(self, request, *args, **kwargs):
        try:
            request_method = request.method.lower()
            data = self.parse_body(request)

            show_graphiql = request_method == 'get' and self.should_display_graphiql(request)
            catch = show_graphiql

            pretty = self.pretty or show_graphiql or request.args.get('pretty')

            if request_method != 'options':
                execution_results, all_params = run_http_query(
                    self.schema,
                    request_method,
                    data,
                    query_data=request.args,
                    batch_enabled=self.batch,
                    catch=catch,

                    # Execute options
                    return_promise=self._enable_async,
                    root_value=self.get_root_value(request),
                    context_value=self.get_context(request),
                    middleware=self.get_middleware(request),
                    executor=self.get_executor(request),
                )
                awaited_execution_results = await Promise.all(execution_results)
                result, status_code = encode_execution_results(
                    awaited_execution_results,
                    is_batch=isinstance(data, list),
                    format_error=self.format_error,
                    encode=partial(self.encode, pretty=pretty)
                )

                if show_graphiql:
                    return await self.render_graphiql(
                        params=all_params[0],
                        result=result
                    )

                return HTTPResponse(
                    result,
                    status=status_code,
                    content_type='application/json'
                )

            else:
                return self.process_preflight(request)

        except HttpQueryError as e:
            return HTTPResponse(
                self.encode({
                    'errors': [default_format_error(e)]
                }),
                status=e.status_code,
                headers=e.headers,
                content_type='application/json'
            )

    # noinspection PyBroadException
    def parse_body(self, request):
        content_type = self.get_mime_type(request)
        if content_type == 'application/graphql':
            return {'query': request.body.decode('utf8')}

        elif content_type == 'application/json':
            return load_json_body(request.body.decode('utf8'))

        elif content_type in ('application/x-www-form-urlencoded', 'multipart/form-data'):
            return request.form

        return {}

    @staticmethod
    def get_mime_type(request):
        # We use mimetype here since we don't need the other
        # information provided by content_type
        if 'content-type' not in request.headers:
            return None

        mimetype, _ = parse_header(request.headers['content-type'])
        return mimetype

    def should_display_graphiql(self, request):
        if not self.graphiql or 'raw' in request.args:
            return False

        return self.request_wants_html(request)

    def request_wants_html(self, request):
        accept = request.headers.get('accept', {})
        return 'text/html' in accept or '*/*' in accept

    def process_preflight(self, request):
        """ Preflight request support for apollo-client
        https://www.w3.org/TR/cors/#resource-preflight-requests """
        origin = request.headers.get('Origin', '')
        method = request.headers.get('Access-Control-Request-Method', '').upper()

        if method and method in self.methods:
            return HTTPResponse(
                status=200,
                headers={
                    'Access-Control-Allow-Origin': origin,
                    'Access-Control-Allow-Methods': ', '.join(self.methods),
                    'Access-Control-Max-Age': str(self.max_age),
                }
            )
        else:
            return HTTPResponse(
                status=400,
            )
