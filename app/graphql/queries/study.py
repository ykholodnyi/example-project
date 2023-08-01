import graphene
from sqlalchemy.orm import joinedload

from app.graphql.mixins import CRUMixin
from app.graphql.types.study import StudyType
from app.models import Study


class StudyQuery(CRUMixin):
    study = graphene.Field(
        StudyType,
        study_id=graphene.ID())

    studies = graphene.List(StudyType)

    @classmethod
    def resolve_study(cls, _, info, study_id):
        return cls.get_object(obj_id=study_id, model=Study, session=info.context["request"].state.db)

    @classmethod
    def resolve_studies(cls, _, info):
        return info.context["request"].state.db.query(Study).options(
            joinedload(Study.bookings),
        ).all()
