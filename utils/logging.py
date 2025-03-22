import logging
from logging import getLogger, Logger, Formatter, handlers, DEBUG, basicConfig, INFO
from os import path
from pathlib import Path
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


class Colour:
    BLACK = '\x1b[30m'
    RED = '\x1b[31m'
    GREEN = '\x1b[32m'
    YELLOW = '\x1b[33m'
    BLUE = '\x1b[34m'
    MAGENTA = '\x1b[35m'
    CYAN = '\x1b[36m'
    WHITE = '\x1b[37m'


class Background:
    BLACK = '\x1b[40m'
    RED = '\x1b[41m'
    GREEN = '\x1b[42m'
    YELLOW = '\x1b[43m'
    BLUE = '\x1b[44m'
    MAGENTA = '\x1b[45m'
    CYAN = '\x1b[46m'
    WHITE = '\x1b[47m'


class Bright:
    BLACK = '\x1b[90m'
    RED = '\x1b[91m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    BLUE = '\x1b[94m'
    MAGENTA = '\x1b[95m'
    CYAN = '\x1b[96m'
    WHITE = '\x1b[97m'


class BrightBackground:
    BLACK = '\x1b[100m'
    RED = '\x1b[101m'
    GREEN = '\x1b[102m'
    YELLOW = '\x1b[103m'
    BLUE = '\x1b[104m'
    MAGENTA = '\x1b[105m'
    CYAN = '\x1b[106m'
    WHITE = '\x1b[107m'


class Style:
    BOLD = '\x1b[1m'
    DIM = '\x1b[2m'
    UNDERLINE = '\x1b[4m'
    RESET = '\x1b[0m'


class ColourFormatter(Formatter):
    LEVEL_COLOURS = [(logging.DEBUG, Colour.CYAN), (logging.INFO, Colour.BLUE),
                     (logging.WARNING, Colour.YELLOW + Style.BOLD), (logging.ERROR, Colour.RED + Style.BOLD),
                     (logging.CRITICAL, Bright.RED + Style.BOLD + Style.UNDERLINE)]

    FORMATS = {level: logging.Formatter(
        f"{BrightBackground.BLACK}%(asctime)s{Style.RESET}{colour}%(levelname)-8s{Style.RESET + Colour.MAGENTA} %(name)s{Style.RESET} %(message)s",
        '%Y-%m-%d %H:%M:%S', ) for level, colour in LEVEL_COLOURS}

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        output = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output


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

    logging.root.handlers[0].setFormatter(ColourFormatter())

    if logs_path is not None:
        # If logs_path is a relative path, we move to project root first. If this is undesirable, remove this block.
        # I found this useful because I can run the bot from any directory, while still having the logs in the same place.
        if not path.isabs(logs_path):
            logs_path = path.join(path.dirname(path.realpath(__file__)), "..", logs_path)

        logs_path = Path(logs_path).resolve()

        if not logs_path.exists():
            logs_path.mkdir(parents=True, exist_ok=True)

        file_handler = handlers.RotatingFileHandler(filename=f"{logs_path}/discord.log", encoding="utf-8",
                                                    maxBytes=32 * 1024 * 1024, backupCount=5)
        file_handler.setFormatter(formatter)

        file_handler.setLevel(DEBUG if debug else INFO)

        # We add the handler to the discord logger. This automatically applies to all child loggers. (e.g. discord.bot)
        getLogger(get_logger_base_name()).addHandler(file_handler)

    getLogger(get_logger_base_name()).setLevel(DEBUG if debug else INFO)
