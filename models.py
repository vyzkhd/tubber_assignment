from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, VARCHAR
from sqlalchemy.dialects.postgresql import JSON

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"

    userid = Column(Integer, index=True)
    ts = Column(String,)
    latlong = Column(String,)
    noun = Column(VARCHAR(length=10))
    verb = Column(VARCHAR(length=10))
    timespent = Column(Integer,)
    properties = Column(JSON,)
