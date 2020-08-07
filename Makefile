dev-setup:
	python pip install -e ".[test]"

tests:
	py.test tests --cov=sanic_graphql -vv