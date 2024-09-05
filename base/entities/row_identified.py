from sqlalchemy import Column, Integer


class RowIdentified:
    """
    Base class for tables that are identified by an auto-incrementing row id.
    """
    row_id = Column(Integer, primary_key=True, autoincrement=True)
