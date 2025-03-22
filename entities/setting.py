from typing import Optional

from sqlalchemy import Column, String

from entities import Base


class Setting(Base):
    """
    Table for storing ad-hoc bot & cog Settings.
    This table is used to store key-value pairs used for random settings / saved values in cogs.
    """
    __tablename__ = "Settings"

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False, default="")


settings_cache = {}


def get_all_settings() -> list:
    """
    Get all settings from the database.
    :return: A list of all settings.
    """
    return Setting.query.all()


def get_setting(key: str, default_value: Optional[str] = None) -> Optional[str]:
    """
    Get a setting from the database.
    :param key: The key of the setting.
    :param default_value: The default value of the setting.
    :return: The value of the setting.
    """
    if key in settings_cache:
        return settings_cache[key]

    setting = Setting.query.filter_by(key=key).first()

    if setting is None:
        return default_value

    settings_cache[key] = setting.value

    return settings_cache[key] or default_value


def set_setting(bot, key: str, value: str) -> None:
    """
    Set a setting in the database.
    :param bot: The bot instance.
    :param key: The key of the setting.
    :param value: The value of the setting.
    """
    setting = Setting.query.filter_by(key=key).first()

    if setting is None:
        setting = Setting(key=key, value=value)
        bot.database_session.add(setting)
    else:
        setting.value = value

    bot.database_session.commit()

    settings_cache[key] = value
