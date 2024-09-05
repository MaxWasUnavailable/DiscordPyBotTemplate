import logging
from datetime import datetime, timedelta
from typing import Optional

from discord import Intents, Message
from discord.ext import commands
from discord.ext.tasks import loop
from discord.utils import MISSING

from core.config import BotConfig
from database.database_handler import DatabaseHandler
from utils.logging import get_logger


class MyBot(commands.Bot):
    """
    Custom bot class that inherits from discord.commands.Bot. Extends some functionality, and initialises custom systems.
    """

    def __init__(self, config: BotConfig, *args, **kwargs):
        """
        Initialize the bot.
        :param config: Config used for the bot.
        """
        kwargs["intents"] = kwargs.get("intents", Intents.all())
        kwargs["case_insensitive"] = kwargs.get("case_insensitive", True)
        kwargs["command_prefix"] = kwargs.get("command_prefix", commands.when_mentioned_or("!"))

        self.config = config

        self.database_handler = DatabaseHandler(config.database_url)

        self.logger = get_logger()

        self.start_time = datetime.now()
        self.started = False

        super().__init__(*args, **kwargs)

    def run(self, token: str, *, reconnect: bool = True, log_handler: Optional[logging.Handler] = MISSING,
            log_formatter: logging.Formatter = MISSING, log_level: int = MISSING, root_logger: bool = False, ) -> None:
        self.start_time = datetime.now()
        super().run(token, reconnect=reconnect, log_handler=log_handler, log_formatter=log_formatter,
                    log_level=log_level, root_logger=root_logger)

    @property
    def uptime(self) -> timedelta:
        """
        Returns the bot's uptime.
        """
        return datetime.now() - self.start_time

    @property
    def database_session(self):
        """
        Returns the database session.
        """
        return self.database_handler.session

    async def on_message(self, message: Message, /) -> None:
        """
        Override the on_message method to ignore messages from bots.
        :param message: The message.
        """
        if message.author.bot:
            return

        await super().on_message(message)

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        """
        Start the bot.
        :param token: The bot's token.
        :param reconnect: Whether to reconnect after disconnection.
        """
        self.logger.info("Bot is starting...")

        await super().start(token=token, reconnect=reconnect)

    async def close(self) -> None:
        """
        Close the bot.
        """
        self.logger.info(f"Bot is shutting down. Uptime: {self.uptime}")

        if self.database_handler:
            self.database_handler.close()

        await super().close()

    async def handle_initial_ready(self):
        """
        Handle the first ready event (after the bot has started).
        """
        await self.init_extensions()

        self.database_handler.initialise_database()

        await self.post_init_extensions()

        self.commit_loop.start()

        self.started = True

    async def on_ready(self):
        if not self.started:
            await self.handle_initial_ready()
            self.logger.info(f"Bot is ready. Logged in as {self.user}. Boot time: {self.uptime}")
        else:
            self.logger.info("Bot has reconnected.")

    async def on_disconnect(self):
        self.logger.warning("Bot has disconnected.")

    async def on_resume(self):
        self.logger.info("Bot has resumed.")

    async def init_extensions(self):
        """
        Load all extensions.
        """
        for extension in self.config.extensions:
            try:
                await self.load_extension(f"{self.config.extensions_path}.{extension}")
                self.logger.info(f"Loaded extension: {extension}")
            except Exception as e:
                self.logger.exception(f"Failed to load extension: {extension}", exc_info=e)

    async def post_init_extensions(self):
        """
        Post-initialise all extensions.
        """
        self.logger.info("Post-initialising extensions...")
        for extension in self.cogs:
            try:
                cog = self.get_cog(extension)
                if hasattr(cog, "post_init"):
                    await cog.post_init()
                    self.logger.info(f"Post-initialised extension: {extension}")
            except Exception as e:
                self.logger.exception(f"Failed to post-initialise extension: {extension}", exc_info=e)

    @loop(hours=6, reconnect=True)
    async def commit_loop(self):
        """
        Commit the database session every loop. Automatically retries on failure.
        """
        self.logger.info("Committing database session...")
        try:
            self.database_session.commit()
            self.logger.info("Database session committed.")
        except Exception as e:
            self.logger.error(f"Failed to commit database session: {e}")
