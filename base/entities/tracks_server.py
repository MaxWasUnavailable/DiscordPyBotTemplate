from sqlalchemy import Column, Integer


class TracksServer:
    """
    Base class for tables that track a Server id.
    """
    server_id = Column(Integer)
