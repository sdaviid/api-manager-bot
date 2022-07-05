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
    date_created = Column(DateTime, default=datetime.utcnow())


    @classmethod
    def add(cls, session, hash):
        source = Source()
        source.hash = hash
        session.add(source)
        session.commit()
        session.refresh(source)
        return Source.find_by_id(session=session, id=source.id)
