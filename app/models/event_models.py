from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    time = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # This is added in case we want to stop events with the same time and description being created; to include it
    # simply uncomment and run a new migration
    # __table_args__ = (UniqueConstraint('description', 'time', name='_description_time_uc'),)
