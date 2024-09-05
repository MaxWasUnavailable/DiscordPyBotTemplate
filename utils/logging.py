from logging import getLogger, Logger, Formatter, handlers, DEBUG, basicConfig, INFO
from os import path, mkdir
from typing import Optional


def get_logger_base_name() -> str:
    """
    Get the base name of the logger.
    :return: The base name of the logger.
    """
    return "discord"


def get_logger_bot_name() -> str:
    """
    Get the name of the bot logger.
    :return: The name of the bot logger.
    """
    return f"{get_logger_base_name()}.bot"


def get_logger_name(postfix: Optional[str] = "") -> str:
    """
    Get the name of the logger.
    :param postfix: The postfix.
    :return: The name of the logger.
    """
    return f"{get_logger_bot_name()}{"." + postfix if postfix else ""}"


def get_logger_qualified_name(entity: object) -> str:
    """
    Get the qualified name of the logger for some entity.
    :return: The qualified name of the logger.
    """
    if not hasattr(entity, "__qualname__"):
        entity = entity.__class__

    return get_logger_name(entity.__qualname__)


def get_logger() -> Logger:
    """
    Get the default logger.
    :return: Logger.
    """
    return getLogger(get_logger_name())


def get_logger_for(entity: object) -> Logger:
    """
    Get the logger for some entity.
    :param entity: The entity.
    :return: Logger.
    """
    return getLogger(get_logger_qualified_name(entity))


def init_logging(logs_path: Optional[str] = None, debug: Optional[bool] = False) -> None:
    """
    Initialise logging.
    :param logs_path: The path to the logs.
    :param debug: Whether to enable debug logging.
    """
    datetime_format = "%Y-%m-%d %H:%M:%S"
    formatter = Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", style="{", datefmt=datetime_format)

    basicConfig(level=DEBUG if debug else INFO, format="[{asctime}] [{levelname:<8}] {name}: {message}", style="{",
                datefmt=datetime_format)

    if logs_path is not None:
        # If logs_path is a relative path, we move to project root first. If this is undesirable, remove this block.
        # I found this useful because I can run the bot from any directory, while still having the logs in the same place.
        if not path.isabs(logs_path):
            logs_path = path.join(path.dirname(path.realpath(__file__)), "..", logs_path)

        if not path.exists(logs_path):
            mkdir(logs_path)

        file_handler = handlers.RotatingFileHandler(filename=f"{logs_path}/discord.log", encoding="utf-8",
                                                    maxBytes=32 * 1024 * 1024, backupCount=5)
        file_handler.setFormatter(formatter)

        file_handler.setLevel(DEBUG if debug else INFO)

        # We add the handler to the discord logger. This automatically applies to all child loggers. (e.g. discord.bot)
        getLogger(get_logger_base_name()).addHandler(file_handler)

    getLogger(get_logger_base_name()).setLevel(DEBUG if debug else INFO)
