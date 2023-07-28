import enum

from graphql import GraphQLError


class ErrorCodes(enum.Enum):
    NOT_FOUND = "NOT_FOUND"


class DefaultGQLError(GraphQLError):
    def __init__(self, error_str: str = "Server error", *args, **kwargs):
        """Adding default error string to GraphQLError"""
        super().__init__(error_str, *args, **kwargs)
