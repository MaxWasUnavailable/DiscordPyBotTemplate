import discord

from extensions.command_logging.command_logging_cog import CommandLoggingCog


class UsingMasterLogMixin:
    """
    Mixin class for cogs that need to log actions to the master log channel.

    This mixin needs to be added to a class that also has the BaseCog as a parent.
    """
    command_logging_cog_cache = None

    def get_command_logging_cog(self) -> CommandLoggingCog:
        """
        Get the CommandLoggingCog.
        :return: The CommandLoggingCog.
        """
        if self.command_logging_cog_cache is not None:
            return self.command_logging_cog_cache

        command_logging_cog: CommandLoggingCog = self.bot.get_cog(CommandLoggingCog.__name__)
        if command_logging_cog is None:
            raise Exception("CommandLoggingCog not found.")

        self.command_logging_cog_cache = command_logging_cog
        return command_logging_cog


    async def master_log_user_action(self, user: discord.Member, log: str):
        """
        Log a user action to the master log channel.
        :param user: The user.
        :param log: The log.
        """
        embed = discord.Embed(title="User Action", description=log, color=0x0000ff)
        embed.set_author(name=user.display_name, icon_url=user.avatar.url)
        await self.get_command_logging_cog().send_master_log(embed=embed)

    async def master_log(self, log: str):
        """
        Send a log to the master log channel.
        :param log: The log.
        """
        embed = discord.Embed(title="Log", description=log, color=0x0000ff)
        await self.get_command_logging_cog().send_master_log(embed=embed)

    async def master_error_log(self, log: str):
        """
        Send an error log to the master log channel.
        :param log: The log.
        """
        embed = discord.Embed(title="Error Log", description=log, color=0xff0000)
        await self.get_command_logging_cog().send_master_log(embed=embed)
