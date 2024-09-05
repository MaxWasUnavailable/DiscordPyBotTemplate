from sqlalchemy import Column, DateTime, func


class TracksUpdate:
    """
    Base class for tables that track when an entry is updated.
    """
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
