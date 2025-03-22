from typing import Optional

from sqlalchemy import Column, String

from base.entities.server_identified import ServerIdentified
from entities import Base


class ServerSetting(Base, ServerIdentified):
    """
    Table for storing server-specific settings.
    """
    __tablename__ = "ServerSettings"

    key = Column(String, nullable=False)
    value = Column(String, nullable=False, default="")


server_settings_cache = {}


def get_setting(server_id: int, key: str, default_value: Optional[str] = None) -> Optional[str]:
    """
    Get a setting from the database.
    :param server_id: The ID of the server.
    :param key: The key of the setting.
    :param default_value: The default value of the setting.
    :return: The value of the setting.
    """
    setting_key = (server_id, key)
    if setting_key in server_settings_cache:
        return server_settings_cache[setting_key]

    setting = ServerSetting.query.filter_by(server_id=server_id, key=key).first()

    if setting is None:
        return default_value

    server_settings_cache[setting_key] = setting.value

    return server_settings_cache[setting_key] or default_value


def set_setting(bot, server_id: int, key: str, value: str) -> None:
    """
    Set a setting in the database.
    :param bot: The bot instance.
    :param server_id: The ID of the server.
    :param key: The key of the setting.
    :param value: The value of the setting.
    """
    setting = ServerSetting.query.filter_by(server_id=server_id, key=key).first()

    if setting is None:
        setting = ServerSetting(server_id=server_id, key=key, value=value)
        bot.session.add(setting)
    else:
        setting.value = value

    bot.session.commit()

    server_settings_cache[(server_id, key)] = value
