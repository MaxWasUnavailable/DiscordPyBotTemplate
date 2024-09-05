from sqlalchemy import Column, Boolean, Integer, String, DateTime, func

from base.entities.tracks_creation import TracksCreation
from base.entities.tracks_update import TracksUpdate
from base.entities.user_identified import UserIdentified
from . import Base


class ExampleTable(UserIdentified, TracksCreation, TracksUpdate, Base):
    """
    Example showing how to create a table in the database. Only once imported, will it be created by the database handler.
    """
    __tablename__ = "ExampleTable"

    example_column = Column(Boolean, default=False)
    example_column_2 = Column(Integer, default=0)
    example_column_3 = Column(String, default="")
    example_column_4 = Column(DateTime, default=func.now())
