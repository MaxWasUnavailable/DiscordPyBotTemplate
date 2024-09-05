from discord.ext import commands

from core.bot import MyBot
from utils.logging import get_logger_for


class BaseCog(commands.Cog):
    """
    BaseCog is a base class for cogs that provides some common functionality.
    """

    def __init__(self, bot: MyBot):
        """
        :param bot: Bot instance.
        """
        self.bot = bot
        self.logger = get_logger_for(self)

        self.logger.debug("Object initialised.")

    async def post_init(self):
        """
        This method is called after the cog has been initialised.
        Useful for setting up any additional functionality that requires other cogs, database tables, etc.
        """
        pass

    async def cog_load(self) -> None:
        """
        This method is called when the cog is loaded.
        """
        self.logger.info(f"Cog initialised.")
