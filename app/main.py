import logging.config

from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp
from fastapi_middleware import SQLQueriesMiddleware, RequestVarsMiddleware

from app.config import settings
from app.graphql import graphql_schema


# Load the logging configuration from logging.conf file
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logging.getLogger("fastapi-middleware").setLevel(logging.DEBUG)

app = FastAPI()


logger = logging.getLogger(__name__)
logger.info(f'DEBUG: {settings.DEBUG}, type: {type(settings.DEBUG)}')

if settings.DEBUG:
    app.add_middleware(SQLQueriesMiddleware)
    app.add_middleware(RequestVarsMiddleware)

app.add_route(
    "/graphql",
    GraphQLApp(
        schema=graphql_schema,
    )
)


