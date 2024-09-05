from .command_logging_cog import setup as cog_setup


async def setup(bot) -> None:
    """
    Set up the extension.
    :param bot: The bot instance.
    """
    await cog_setup(bot)
