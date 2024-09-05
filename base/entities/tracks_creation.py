from sqlalchemy import Column, DateTime, func


class TracksCreation:
    """
    Base class for tables that track when an entry is created.
    """
    created_at = Column(DateTime, nullable=False, default=func.now())
