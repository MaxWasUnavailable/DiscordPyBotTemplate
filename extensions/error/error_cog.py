from discord import Interaction
from discord import app_commands
from discord.ext import commands

from base.base_cog import BaseCog
from core.bot import MyBot


class ErrorCog(BaseCog):
    """
    ErrorCog is a cog that handles command errors.
    """

    command_error_messages = {commands.CommandNotFound: "Command not found: `{}`.",
                              commands.MissingRequiredArgument: "Missing required argument: `{}`.",
                              commands.BadArgument: "Bad argument.",
                              commands.CommandOnCooldown: "You are on cooldown. Try again in `{:.2f}` seconds.",
                              commands.TooManyArguments: "Too many arguments.",
                              commands.MissingPermissions: "You are not allowed to use this command.",
                              commands.BotMissingPermissions: "I am not allowed to use this command.",
                              commands.NoPrivateMessage: "This command can only be used in a server.",
                              commands.NotOwner: "You are not the owner of this bot.",
                              commands.DisabledCommand: "This command is disabled.",
                              commands.CheckFailure: "You do not have permission to use this command."}

    app_command_error_messages = {app_commands.CommandNotFound: "Command not found: `{}`.",
                                  app_commands.CommandOnCooldown: "You are on cooldown. Try again in `{:.2f}` seconds.",
                                  app_commands.MissingPermissions: "You are not allowed to use this command.",
                                  app_commands.BotMissingPermissions: "I am not allowed to use this command.",
                                  app_commands.NoPrivateMessage: "This command can only be used in a server.",
                                  app_commands.CheckFailure: "You do not have permission to use this command."}

    def __init__(self, bot: MyBot) -> None:
        super().__init__(bot)

        self.bot.tree.on_error = self.on_app_command_error

    def get_command_error_message(self, error: commands.CommandError) -> str:
        """
        Get the error message for the given error.
        :param error: Error.
        :return: Error message.
        """
        return self.command_error_messages.get(type(error), "An unknown error occurred.")

    def get_app_command_error_message(self, error: app_commands.AppCommandError) -> str:
        """
        Get the error message for the given error.
        :param error: Error.
        :return: Error message.
        """
        return self.app_command_error_messages.get(type(error), "An unknown error occurred.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """
        Event that triggers when a command fails.
        :param ctx: Context.
        :param error: Error.
        """
        self.logger.error(f"{ctx.command} called by {ctx.author} raised an exception: {error}. ({ctx.message})")

        error_message = self.get_command_error_message(error)

        if isinstance(error, commands.CommandNotFound):
            error_message = error_message.format(ctx.invoked_with)

        elif isinstance(error, commands.MissingRequiredArgument):
            error_message = error_message.format(error.param.name)

        elif isinstance(error, commands.CommandOnCooldown):
            error_message = error_message.format(error.retry_after)

        await ctx.reply(error_message)

        if self.bot.is_owner(ctx.author):
            await ctx.author.send(f"An error occurred while running the command `{ctx.command.name}`: {error}")

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: Interaction, error: app_commands.AppCommandError) -> None:
        """
        Event that triggers when a command fails.
        :param interaction: The interaction object.
        :param error: The exception.
        """
        if interaction.command is None:
            self.logger.error(f"Command not found: {interaction.data}.")
            await interaction.response.send_message(f"Command not found: `{interaction.data.get('name')}`.",
                                                    ephemeral=True)
            return

        self.logger.error(f"{interaction.command.name} called by {interaction.user} raised an exception: {error}.")

        error_message = self.get_app_command_error_message(error)

        if isinstance(error, app_commands.CommandNotFound):
            error_message = error_message.format(interaction.command.name)

        elif isinstance(error, app_commands.CommandOnCooldown):
            error_message = error_message.format(error.retry_after)

        try:
            await interaction.response.send_message(error_message, ephemeral=True)
        except:
            await interaction.followup.send(error_message, ephemeral=True)

        if self.bot.is_owner(interaction.user):
            await interaction.user.send(
                f"An error occurred while running the command `{interaction.command.name}`: {error}")


async def setup(bot):
    await bot.add_cog(ErrorCog(bot))


async def teardown(bot):
    await bot.remove_cog(ErrorCog.__name__)
