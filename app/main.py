import logging.config

from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp
from fastapi_middleware import SQLQueriesMiddleware, RequestVarsMiddleware

from app.config import settings
from app.graphql import graphql_schema
from app.middleware import DBSessionMiddleware

# Load the logging configuration from logging.conf file
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

app = FastAPI()

if settings.DEBUG:
    logging.getLogger("fastapi-middleware").setLevel(logging.DEBUG)
    app.add_middleware(SQLQueriesMiddleware)
    app.add_middleware(RequestVarsMiddleware)

app.add_middleware(DBSessionMiddleware)

app.add_route(
    "/graphql",
    GraphQLApp(
        schema=graphql_schema,
    )
)
