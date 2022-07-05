from datetime import date
from pydantic import Field
from datetime import datetime
from app.models.schemas.base import baseSchema


class SourceAdd(baseSchema):
    hash: str
    status: str
    



class SourceDetail(baseSchema):
    id: int
    hash: str
    status: str
    