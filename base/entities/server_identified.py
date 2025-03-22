from sqlalchemy import Column, Integer


class ServerIdentified:
    """
    Base class for tables that are identified by a Server id
    """
    server_id = Column(Integer, primary_key=True)
