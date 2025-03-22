from typing import Optional

from sqlalchemy import Column, String

from base.entities.user_identified import UserIdentified
from entities import Base


class UserSetting(Base, UserIdentified):
    """
    Table for storing user-specific settings.
    """
    __tablename__ = "UserSettings"

    key = Column(String, nullable=False)
    value = Column(String, nullable=False, default="")


user_settings_cache = {}


def get_setting(user_id: int, key: str, default_value: Optional[str] = None) -> Optional[str]:
    """
    Get a setting from the database.
    :param user_id: The ID of the user.
    :param key: The key of the setting.
    :param default_value: The default value of the setting.
    :return: The value of the setting.
    """
    setting_key = (user_id, key)
    if setting_key in user_settings_cache:
        return user_settings_cache[setting_key]

    setting = UserSetting.query.filter_by(user_id=user_id, key=key).first()

    if setting is None:
        return default_value

    user_settings_cache[setting_key] = setting.value

    return user_settings_cache[setting_key] or default_value


def set_setting(bot, user_id: int, key: str, value: str) -> None:
    """
    Set a setting in the database.
    :param bot: The bot instance.
    :param user_id: The ID of the user.
    :param key: The key of the setting.
    :param value: The value of the setting.
    """
    setting = UserSetting.query.filter_by(user_id=user_id, key=key).first()

    if setting is None:
        setting = UserSetting(user_id=user_id, key=key, value=value)
        bot.session.add(setting)
    else:
        setting.value = value

    bot.session.commit()

    user_settings_cache[(user_id, key)] = value
