"""
Config class allowing for hierarchical configuration settings.
"""

import os
from typing import Any, Dict, Optional, List

from dotenv import load_dotenv
from yaml import safe_load


class BotConfig(dict):
    """
    Configuration settings for the bot.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialise the configuration settings.
        :param config: The configuration settings.
        """
        self.__pre_populate()
        super().__init__(config or {})

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a configuration setting. Keys are case-insensitive to allow for different format conventions.
        :param key: The key.
        :param value: The value.
        """
        super().__setitem__(key.lower(), value)

    def update(self, __m, **kwargs):
        """
        Update the configuration settings. Keys are case-insensitive to allow for different format conventions.
        :param __m: The dictionary to update from.
        :param kwargs: Additional keyword arguments.
        """
        super().update({key.lower(): value for key, value in __m.items()}, **kwargs)

    def __pre_populate(self) -> None:
        """
        Pre-populate the dictionary for filtering purposes.
        """
        self["bot_token"] = ""
        self["database_url"] = ""
        self["logs_path"] = "logs"
        self["debug"] = False
        self["extensions_path"] = "extensions"
        self["extensions"] = []

    def filter_relevant(self, in_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter out irrelevant keys from a dictionary. Used to filter out irrelevant environment variables.
        :param in_data: The dictionary.
        :return: The filtered dictionary.
        """
        out_dict = {}
        for key in in_data.keys():
            if key.lower() in self.keys():
                out_dict[key] = in_data[key]

        return out_dict

    @property
    def token(self) -> str:
        """
        Get the bot token.
        :return: The bot token.
        """
        return self.get("bot_token", "")

    @property
    def database_url(self) -> str:
        """
        Get the database URL.
        :return: The database URL.
        """
        return self.get("database_url", "")

    @property
    def logs_path(self) -> str:
        """
        Get the logs path.
        :return: The logs path.
        """
        return self.get("logs_path", "./logs")

    @property
    def debug(self) -> bool:
        """
        Get the debug setting.
        :return: The debug setting.
        """
        return self.get("debug", False)

    @property
    def extensions_path(self) -> str:
        """
        Get the extensions path.
        :return: The extensions path.
        """
        return self.get("extensions_path", "extensions")

    @property
    def extensions(self) -> List[str]:
        """
        Get the list of extensions to load.
        :return: The list of extensions to load.
        """
        return self.get("extensions", [])

    def update_from_yaml(self, path: str) -> "BotConfig":
        """
        Update configuration settings from a YAML file.
        :param path: The path to the YAML file.
        """
        if not os.path.exists(path):
            return self

        with open(path, "r") as file:
            self.update(safe_load(file))

        return self

    @classmethod
    def from_yaml(cls, path: str) -> "BotConfig":
        """
        Load configuration settings from a YAML file.
        :param path: The path to the YAML file.
        :return: The configuration settings.
        """
        return cls().update_from_yaml(path)

    def update_from_dot_env(self, path: str) -> "BotConfig":
        """
        Update configuration settings from a .env file.
        :param path: The path to the .env file.
        """
        if not os.path.exists(path):
            return self

        load_dotenv(path)
        self.update(self.filter_relevant(os.environ))

        return self

    @classmethod
    def from_dot_env(cls, path: str) -> "BotConfig":
        """
        Load configuration settings from a .env file.
        :param path: The path to the .env file.
        :return: The configuration settings.
        """
        return cls().update_from_dot_env(path)

    def update_from_env(self) -> "BotConfig":
        """
        Update configuration settings from environment variables.
        """
        self.update(self.filter_relevant(os.environ))
        return self

    @classmethod
    def from_env(cls) -> "BotConfig":
        """
        Load configuration settings from environment variables.
        :return: The configuration settings.
        """
        return cls().update_from_env()

    def update_from_dict(self, config: Dict[str, Any]) -> "BotConfig":
        """
        Update configuration settings from a dictionary.
        :param config: The dictionary.
        """
        self.update(config)
        return self

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "BotConfig":
        """
        Load configuration settings from a dictionary.
        :param config: The dictionary.
        :return: The configuration settings.
        """
        return cls().update_from_dict(config)

    @classmethod
    def from_hierarchy(cls, config_path: Optional[str] = None, env_path: Optional[str] = None,
                       commandline_args: Optional[Dict[str, Any]] = None) -> "BotConfig":
        """
        Load configuration settings from a hierarchy of sources.
        :param config_path: The path to the YAML file.
        :param env_path: The path to the .env file.
        :param commandline_args: The commandline arguments.
        :return: The configuration settings.
        """
        return cls().update_from_yaml(config_path).update_from_dot_env(env_path).update_from_env().update_from_dict(
            commandline_args or {})
