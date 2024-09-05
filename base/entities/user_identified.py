from sqlalchemy import Column, Integer


class UserIdentified:
    """
    Base class for tables that are identified by a Discord user id.
    """
    user_id = Column(Integer, primary_key=True)
