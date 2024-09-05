import discord
from discord.ext import commands

from base.base_cog import BaseCog
from core.bot import MyBot


class CommandLoggingCog(BaseCog):
    """
    CommandLoggingCog is a cog that logs command usage.
    """

    def __init__(self, bot: MyBot) -> None:
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context) -> None:
        """
        Event that triggers when a command is successfully run.
        :param ctx: Context.
        """
        if ctx.interaction:
            # Called as app command. Prevent logging twice.
            return
        self.logger.info(f"{ctx.command} called successfully by {ctx.author}.")

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction,
                                        command: discord.app_commands.Command) -> None:
        """
        Event that triggers when a command is successfully run.
        :param interaction: The interaction object.
        :param command: The command object.
        """
        self.logger.info(f"{command.name} called successfully by {interaction.user}.")


async def setup(bot):
    await bot.add_cog(CommandLoggingCog(bot))


async def teardown(bot):
    await bot.remove_cog(CommandLoggingCog.__name__)
