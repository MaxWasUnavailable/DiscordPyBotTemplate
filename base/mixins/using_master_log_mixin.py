import discord

from extensions.master_log.master_log_cog import MasterLogCog


class UsingMasterLogMixin:
    """
    Mixin class for cogs that need to log actions to the master log channel.

    This mixin needs to be added to a class that also has the BaseCog as a parent.
    """
    master_log_cog_cache = None

    def get_master_log_cog(self) -> MasterLogCog:
        """
        Get the MasterLogCog.
        :return: The MasterLogCog.
        """
        if self.master_log_cog_cache is not None:
            return self.master_log_cog_cache

        master_log_cog: MasterLogCog = self.bot.get_cog(MasterLogCog.__name__)
        if master_log_cog is None:
            raise Exception("MasterLogCog not found.")

        self.master_log_cog_cache = master_log_cog
        return master_log_cog

    async def master_log_user_action(self, user: discord.Member, log: str):
        """
        Log a user action to the master log channel.
        :param user: The user.
        :param log: The log.
        """
        embed = discord.Embed(title="User Action", description=log, color=0x0000ff)
        embed.set_author(name=user.display_name, icon_url=user.avatar.url)
        await self.get_master_log_cog().send_master_log(embed=embed)

    async def master_log(self, log: str):
        """
        Send a log to the master log channel.
        :param log: The log.
        """
        embed = discord.Embed(title="Log", description=log, color=0x0000ff)
        await self.get_master_log_cog().send_master_log(embed=embed)

    async def master_error_log(self, log: str):
        """
        Send an error log to the master log channel.
        :param log: The log.
        """
        embed = discord.Embed(title="Error Log", description=log, color=0xff0000)
        await self.get_master_log_cog().send_master_log(embed=embed)
