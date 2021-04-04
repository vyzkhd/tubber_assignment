from pydantic import BaseModel
from typing import Dict

class Event(BaseModel):
    id: int 
    userid: int
    ts: str 
    latlong: str 
    noun: str 
    verb: str 
    timespent: int 
    properties: Dict

    class Config:
        orm_mode = True 
