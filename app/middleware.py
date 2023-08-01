import fastapi
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from app.models.base import SessionLocal


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ):
        """
        Attach a database session to the request state.
        This ensures that each request will have a separate database session attached to it.

        Native FastAPI dependencies (fastapi.Depends) is not used
        since graphene endpoints does not support it.
        """
        try:
            request.state.db = SessionLocal()
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response
