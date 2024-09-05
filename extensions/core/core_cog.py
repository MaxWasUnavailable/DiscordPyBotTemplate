from discord import Interaction
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from base.base_cog import BaseCog
from core.bot import MyBot
from utils.checks.is_owner import is_owner


class CoreCog(BaseCog):
    """
    CoreCog is a cog with core commands such as sync and ping.
    """

    def __init__(self, bot: MyBot) -> None:
        super().__init__(bot)

    async def autocomplete_command_name(self, interaction: Interaction, current: str) -> list[Choice[str]]:
        """
        Autocomplete command names.
        :param interaction: Interaction.
        :param current: Current string.
        :return: List of command names.
        """
        if not hasattr(CoreCog.autocomplete_command_name, "tree_cache"):
            CoreCog.autocomplete_command_name.tree_cache = await self.bot.tree.fetch_commands()

        return [Choice(name=command.name, value=str(command.id)) for command in
                CoreCog.autocomplete_command_name.tree_cache if current.lower() in command.name.lower()]

    @app_commands.command(name="ping", description="Ping the bot.")
    @app_commands.checks.cooldown(2, 60)
    @app_commands.guild_only()
    async def ping(self, interaction: Interaction) -> None:
        """
        Ping the bot.
        :param interaction: Interaction.
        """
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms.", ephemeral=True)

    @commands.hybrid_command(name="sync")
    @app_commands.check(is_owner)
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, current_server: bool = False) -> None:
        """
        Syncs the bot's commands.
        :param ctx: Context.
        :param current_server: Whether to sync the current server only.
        """
        if current_server:
            await self.bot.tree.sync(guild=ctx.guild)
            self.logger.info(f"Sync complete for {ctx.guild}.")
            await ctx.send("Sync complete for current server.")
        else:
            await self.bot.tree.sync()
            self.logger.info(f"Sync complete.")
            await ctx.send("Sync complete.")

    @app_commands.command(name="shutdown", description="Shutdown the bot.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.check(is_owner)
    @app_commands.guild_only()
    async def shutdown(self, interaction: Interaction) -> None:
        """
        Shuts down the bot.
        :param interaction: Interaction.
        """
        self.logger.info(f"Shutdown called by {interaction.user}.")
        await interaction.response.send_message("Shutting down...", ephemeral=True)

        await self.bot.close()

    @app_commands.command(name="generate_command_link", description="Generate a command link.")
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.guild_only()
    @app_commands.autocomplete(command_name=autocomplete_command_name)
    async def generate_command_link(self, interaction: Interaction, command_name: str) -> None:
        """
        Generate a command link.
        :param interaction: Interaction.
        :param command_name: Command name.
        """
        try:
            command_id = int(command_name)
        except ValueError:
            command_id = None

        app_command = await self.bot.tree.fetch_command(command_id) if command_id else None

        if app_command is None:
            for tree_command in await self.bot.tree.fetch_commands():
                if tree_command.name == command_name:
                    app_command = tree_command
                    break

        if app_command is None:
            await interaction.response.send_message(f"Command not found: `{command_name}`.", ephemeral=True)
            return

        await interaction.response.send_message(f"{app_command.mention}")


async def setup(bot):
    await bot.add_cog(CoreCog(bot))


async def teardown(bot):
    await bot.remove_cog(CoreCog.__name__)
