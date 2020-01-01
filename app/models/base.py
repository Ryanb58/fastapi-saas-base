import datetime

from sqlalchemy import Column, DateTime

from app.database import Base


class BaseModel(Base):
    """Base data model for all objects"""

    __abstract__ = True

    created_on = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow)
