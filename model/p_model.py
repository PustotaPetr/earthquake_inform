from pydantic import BaseModel, Field
from datetime import datetime


class EarthQuakeP(BaseModel):
    id: str = Field(alias='publicID')
    description: str = Field(default='')
    time: datetime = Field(default=None)
    longitude: float = Field(default=0)
    latitude: float = Field(default=0)
    depth: int = Field(default=0)
    magnitude: float = Field(default=0)