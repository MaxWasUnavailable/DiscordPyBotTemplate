from typing import Optional, List

import discord
from discord import Embed
from discord import app_commands

from base.base_cog import BaseCog
from base.mixins.using_master_log_mixin import UsingMasterLogMixin
from core.bot import MyBot
from entities.setting import set_setting, get_setting, get_all_settings
from utils.checks.is_owner import is_owner


async def setting_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """
    Autocomplete for the setting command.
    :param interaction: interaction.
    :param current: current input.
    :return: list of autocomplete choices.
    """
    key = current.lower()
    choices = [app_commands.Choice(name=setting.key, value=setting.key) for setting in get_all_settings() if
               key in setting.key.lower()]

    return choices[:25]


class SettingsCog(BaseCog, UsingMasterLogMixin):
    """
    SettingsCog is a cog with commands that allows the bot owner to read and write bot settings.
    """

    def __init__(self, bot: MyBot) -> None:
        super().__init__(bot)

    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.check(is_owner)
    class SettingsCommandGroup(app_commands.Group):
        def __init__(self, *args, **kwargs):
            super().__init__(name="bot-settings", description="Configure settings.", *args, **kwargs)

    settings_group = SettingsCommandGroup()

    @settings_group.command(name="view", description="View a setting. Has autocomplete.")
    @app_commands.autocomplete(key=setting_autocomplete)
    @app_commands.default_permissions(administrator=True)
    @app_commands.check(is_owner)
    async def view_setting(self, interaction: discord.Interaction, key: str) -> None:
        """
        Command to view a bot setting.
        :param interaction: interaction.
        :param key: key of the setting.
        :return: None.
        """
        await self.master_log_user_action(interaction.user, f"Viewed setting: {key}")

        await interaction.response.send_message(
            embed=Embed(title=f"{key}", description=f"{get_setting(key) or 'Setting is not set'}", color=0x0000ff), ephemeral=True)

    @settings_group.command(name="set", description="Set a setting.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.check(is_owner)
    async def setting(self, interaction: discord.Interaction, key: str, value: str) -> None:
        """
        Command to set a bot setting.
        :param interaction: interaction.
        :param key: key of the setting.
        :param value: value of the setting.
        :return: None.
        """
        set_setting(self.bot, key, value)

        await self.master_log_user_action(interaction.user, f"Set setting: {key} to {value}")

        await interaction.response.send_message(
            embed=Embed(title=f"{key}", description=f"{get_setting(key) or 'Setting is not set'}", color=0x0000ff))


async def setup(bot):
    await bot.add_cog(SettingsCog(bot))


async def teardown(bot):
    await bot.remove_cog(SettingsCog.__name__)
