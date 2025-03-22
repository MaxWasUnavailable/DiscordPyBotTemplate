import discord
from discord import app_commands
from discord.ext import commands

from base.base_cog import BaseCog
from core.bot import MyBot
from entities.setting import set_setting, get_setting

from utils.checks.is_owner import is_owner


class CommandLoggingCog(BaseCog):
    """
    CommandLoggingCog is a cog that logs command usage.
    """

    master_log_channel_key = "CommandLoggingCog:master_log_channel_id"

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

    @app_commands.command(name="set-master-log-channel", description="Set the master log channel.")
    @is_owner
    async def set_master_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        """
        Set the master log channel.
        :param channel: The channel to set as the master log channel.
        :param interaction: Interaction.
        """
        set_setting(self.bot, self.master_log_channel_key, str(channel.id))
        await interaction.response.send_message(f"Master log channel set to {channel.mention}.", ephemeral=True)

    async def send_master_log(self, log: str = "", embed: discord.Embed = None):
        """
        Send a log.
        :param log: The log.
        :param embed: The embed.
        """
        master_log_channel_id = get_setting(self.master_log_channel_key)
        if master_log_channel_id is None:
            self.logger.error("Master log channel not set.")
            return
        master_log_channel = self.bot.get_channel(int(master_log_channel_id))
        if master_log_channel is None:
            self.logger.error("Master log channel not found.")
            return

        if embed is None:
            await master_log_channel.send(log)
        else:
            await master_log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CommandLoggingCog(bot))


async def teardown(bot):
    await bot.remove_cog(CommandLoggingCog.__name__)
