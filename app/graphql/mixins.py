import logging
from typing import Any

import graphene
from graphene import InputObjectType
from sqlalchemy import inspect
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import joinedload, subqueryload

from app.graphql.exceptions import DefaultGQLError, ErrorCodes
from app.models.base import RelationshipNotFound, SessionLocal

logger = logging.getLogger(__name__)


class CRUMixin:
    @classmethod
    def get_obj_ref(cls, obj):
        if hasattr(obj, "id"):
            return f"object ID: {obj.id}"
        else:
            return f"object: {type(obj).__name__}"

    @classmethod
    def get_object(cls, obj_id: Any, model, session, eager_load: bool = False):
        try:
            query = session.query(model).filter_by(id=obj_id)
            if eager_load:
                # Get the model's relationships using SQLAlchemy's inspect module
                relationships = inspect(model).relationships
                for relationship in relationships:
                    # Check if the relationship is a many-to-one or one-to-one relationship
                    if relationship.direction.name in ('MANYTOONE', 'ONETOONE'):
                        # Use joinedload for many-to-one or one-to-one relationships
                        query = query.options(joinedload(relationship.key))
                    # subquery load for a one-to-many or many-to-many relationship
                    # does not make sense for a single object

            obj = query.first()

        except DatabaseError as e:
            error_str = f"DatabaseError, object ID: {obj_id}, {e}"
            logger.exception(error_str)
            session.rollback()
            # not exposing the error to the client
            raise DefaultGQLError()

        if obj is None:
            error_str = f"{model.__name__} with ID: {obj_id} does not exist"
            logger.error(error_str)
            # not exposing the error to the client
            raise DefaultGQLError(
                error_str=error_str,
                extensions={"code": ErrorCodes.NOT_FOUND.value})

        return obj

    @classmethod
    def update_object(cls, obj, data: InputObjectType, session: SessionLocal):
        try:
            obj.update(data, session)
            session.commit()

        except DatabaseError as e:
            error_str = f"DatabaseError, {cls.get_obj_ref(obj)}, {e}"
            logger.exception(error_str)
            session.rollback()
            # not exposing the error to the client
            raise DefaultGQLError()

        except RelationshipNotFound as e:
            error_str = f"RelationshipNotFound. {e}"
            logger.info(error_str)
            session.rollback()
            raise DefaultGQLError(
                error_str=error_str,
                extensions={"code": ErrorCodes.NOT_FOUND.value})

        return obj

    @classmethod
    def add_object(cls, obj, session: SessionLocal):
        try:
            session.add(obj)
            session.commit()
        except DatabaseError as e:
            error_str = f"DatabaseError, {cls.get_obj_ref(obj)}, {e}"
            logger.exception(error_str)
            session.rollback()
            # not exposing the error to the client
            raise DefaultGQLError()

        return obj


class IDTypeMixin:
    id = graphene.ID(required=True)

    def resolve_id(self, info):
        return self.id
