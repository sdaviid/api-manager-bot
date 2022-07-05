from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.types import(
    Date,
    Boolean,
    Time,
    DateTime
)
from sqlalchemy.orm import(
    relationship,
    backref
)
from app.models.base import ModelBase
from app.core.database import Base                      
from datetime import datetime

class Source(ModelBase, Base):
    __tablename__ = "source"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hash = Column(String(255))
    status = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())


    @classmethod
    def add(cls, session, hash, status):
        source = Source()
        source.hash = hash
        source.status = status
        session.add(source)
        session.commit()
        session.refresh(source)
        return Source.find_by_id(session=session, id=source.id)


    @classmethod
    def find_by_status(cls, session, status):
        try:
            return session.query(Source).filter_by(status=status).all()
        except Exception as err:
            print(f'model.source.find_by_status exception - {err}')
        return False


    @classmethod
    def update_status(cls, session, id, status):
        source = cls.find_by_id(session=session, id=id)
        if source:
            source.status = status
            session.commit()
            session.refresh(source)
            return source
        return False
