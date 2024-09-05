"""
Database connection and initialisation.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, close_all_sessions

from entities import Base
from utils.logging import get_logger_for


class DatabaseHandler:
    """
    Database handler class.
    """

    def __init__(self, database_url: str):
        """
        Initialise the database handler and create the database connection.
        :param database_url: The database URL. (e.g. postgresql+psycopg2://user:password@localhost:5432/database)
        """
        self.logger = get_logger_for(self)

        self.logger.info("Initialising database connection...")

        if not database_url:
            raise ValueError("Database URL not provided.")

        self.logger.debug("Creating engine...")
        self.database_engine = create_engine(database_url)
        self.logger.debug(f"Engine created: {self.database_engine.url}")

        self.logger.debug("Creating session maker...")
        self.database_session_maker = sessionmaker(bind=self.database_engine)
        self.logger.debug("Session maker created.")

        self.logger.debug("Creating scoped session...")
        self.scoped_session = scoped_session(self.database_session_maker)
        self.logger.debug("Scoped session created.")

        self.logger.info("Database connection initialised.")

    @property
    def session(self):
        """
        Returns the database session.
        """
        return self.scoped_session

    @property
    def engine(self):
        """
        Returns the database engine.
        """
        return self.database_engine

    @property
    def session_maker(self):
        """
        Returns the database session maker.
        """
        return self.database_session_maker

    def initialise_database(self):
        """
        Initialise the database.
        """
        self.logger.info("Initialising database...")

        self.logger.debug("Creating tables...")
        Base.metadata.create_all(self.database_engine, checkfirst=True)
        self.logger.debug("Tables created.")

        self.logger.info("Database initialised.")

    def close(self):
        """
        Close the database connection.
        """
        self.logger.info("Closing database connection...")

        self.scoped_session.commit()
        self.logger.debug("Committed session.")

        self.scoped_session.close()

        close_all_sessions()
        self.database_engine.dispose()

        self.logger.info("Database connection closed.")
