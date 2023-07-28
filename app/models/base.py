from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from app.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=80,
    pool_recycle=60,  # seconds
    pool_timeout=2,  # seconds
)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)


_Base = declarative_base()


class RelationshipNotFound(Exception):
    pass


# abstract base class
class Base(_Base):
    __abstract__ = True

    def update(self, values):
        insp = inspect(self)
        columns = insp.mapper.columns
        relations = insp.mapper.relationships

        for key, value in values.items():
            if key in relations:
                related_class = relations[key].mapper.class_
                if isinstance(value, list):
                    # many-to-many
                    if len(value) == 0:
                        setattr(self, key, [])
                        continue
                    new_relations = db_session.query(related_class).filter(related_class.id.in_(value)).all()
                    if new_relations is None or len(new_relations) == 0:
                        raise RelationshipNotFound(
                            f'Invalid ids: {value} for class {related_class.__name__}, objects not found.')
                    setattr(self, key, new_relations)
                else:
                    # one-to-many, many-to-one, one-to-one
                    new_relation = db_session.query(related_class).filter(related_class.id == value).first()
                    if new_relation is not None:
                        setattr(self, key, new_relation)
                    else:
                        raise RelationshipNotFound(
                            f'Invalid id: {value} for class {related_class.__name__}, object not found.')
            elif key in columns:
                setattr(self, key, value)
