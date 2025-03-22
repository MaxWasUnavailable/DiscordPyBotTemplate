from sqlalchemy import Column, Integer


class TracksUser:
    """
    Base class for tables that track a User id.
    """
    user_id = Column(Integer)
