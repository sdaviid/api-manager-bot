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

class File(ModelBase, Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source_id = Column(Integer)
    name = Column(String(255))
    name_hash = Column(String(255), default=None)
    serve_uri = Column(String(255))
    progress = Column(String(255), default=None)
    status = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())


    @classmethod
    def add(cls, session, source_id, name, status, serve_uri):
        file = File()
        file.source_id = source_id
        file.name = name
        file.status = status
        file.serve_uri = serve_uri
        session.add(file)
        session.commit()
        session.refresh(file)
        return File.find_by_id(session=session, id=file.id)


    @classmethod
    def update_name_hash(cls, session, id, name_hash):
        file = cls.find_by_id(session=session, id=id)
        if file:
            file.name_hash = name_hash
            session.commit()
            session.refresh(file)
            return file
        return False


    @classmethod
    def update_status(cls, session, id, status):
        file = cls.find_by_id(session=session, id=id)
        if file:
            file.status = status
            session.commit()
            session.refresh(file)
            return file
        return False


    @classmethod
    def update_progress(cls, session, id, progress):
        file = cls.find_by_id(session=session, id=id)
        if file:
            file.progress = progress
            session.commit()
            session.refresh(file)
            return file
        return False



    @classmethod
    def find_by_status(cls, session, status):
        try:
            return session.query(File).filter_by(status=status).all()
        except Exception as err:
            print(f'model.file.find_by_status exception - {err}')
        return False


    @classmethod
    def find_by_statuses(cls, session, statuses):
        try:
            return session.query(cls).filter(File.status.in_(statuses)).all()
        except Exception as err:
            print(f'models.file.find_by_statuses exception - {err}')
        return False
