import logging

import graphene

from app.graphql.types.study import (
    StudyType, StudyCreateInputType,
)

from app.models import Study
from app.graphql.mixins import CRUMixin

logger = logging.getLogger(__name__)


class CreateStudy(graphene.Mutation, CRUMixin):
    class Arguments:
        study = graphene.Argument(StudyCreateInputType, required=True)

    study = graphene.Field(StudyType)

    @classmethod
    def mutate(cls, root, info, study, **kwargs):
        obj = Study(**study)
        obj = cls.add_object(obj=obj)
        return CreateStudy(study=obj)
