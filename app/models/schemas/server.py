from datetime import date
from pydantic import Field
from datetime import datetime
from app.models.schemas.base import baseSchema


class ServerAdd(baseSchema):
    hash: str
    



class ServerDetail(baseSchema):
    id: int
    hash: str
    