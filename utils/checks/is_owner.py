from discord import Interaction


async def is_owner(interaction: Interaction) -> bool:
    """
    Check if the interaction user is the owner of the bot.
    :param interaction: Interaction.
    :return: Whether the user is the owner.
    """
    return await interaction.client.is_owner(interaction.user)
