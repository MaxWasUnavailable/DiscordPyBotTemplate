# Discord bot template

> A modern, easily extensible Discord bot template written in Python, using the discord.py library.

---
<p align="center">
  <a href="https://discord.gg/8PJeFeMCsu"><img src="https://img.shields.io/discord/1279890091711398130?logo=discord"></a>
  <a href="https://github.com/MaxWasUnavailable/DiscordPyBotTemplate/releases"><img src="https://img.shields.io/github/v/release/MaxWasUnavailable/DiscordPyBotTemplate"></a>
  <a href="https://github.com/MaxWasUnavailable/DiscordPyBotTemplate/commits/master/"><img src="https://img.shields.io/github/commits-since/MaxWasUnavailable/DiscordPyBotTemplate/latest"></a>
  <a href="https://github.com/MaxWasUnavailable/DiscordPyBotTemplate/commits/master/"><img src="https://img.shields.io/github/last-commit/MaxWasUnavailable/DiscordPyBotTemplate"></a>
  <a href="https://github.com/MaxWasUnavailable/DiscordPyBotTemplate/blob/master/LICENSE"><img src="https://img.shields.io/github/license/MaxWasUnavailable/DiscordPyBotTemplate"></a>
  <a href="https://github.com/MaxWasUnavailable/DiscordPyBotTemplate/fork"><img src="https://img.shields.io/github/forks/MaxWasUnavailable/DiscordPyBotTemplate"></a>
</p>

<p align="center">
  <a href="https://github.com/new?template_name=DiscordPyBotTemplate&template_owner=MaxWasUnavailable">
    <img src="https://img.shields.io/badge/Use this template-29903b?style=for-the-badge&logo=github" alt="Use this template">
  </a>
</p>

## Features

### Extensive config system

The template's config system is hierarchical.

From top to bottom, with lower levels overriding higher levels:

- YAML file (config.yaml)
- .env file
- Environment variables
- Command line arguments

This allows for committable defaults through the YAML file, while keeping sensitive information such as tokens out of
the repository. Environment variables and CLI arguments can be used for testing, Docker deployments, etc.

Of course, you can ignore any of these levels if you don't need them. It is **strongly** recommend to __not__ store
sensitive information such as the bot token in the YAML file, however.

A [BotConfig](core/config.py) class is provided to handle reading and parsing the config, and to provide easy access to
the config values through properties. You can extend this class to add your own config values.

> You are not meant to commit the .env file to the repository, and it is ignored by default. Always be wary of
> committing sensitive / secret information to a repository!

### SQLAlchemy database support

SQLAlchemy is a powerful yet easy-to-use ORM for Python, and I highly recommend making use of it. Benefits include
being able to define and work with database models in a Pythonic way, and not having to write raw SQL queries.
Additionally, you can target multiple different database engines with minimal to no changes to your code, including
simple in-memory databases for testing.

The template includes a simple [database handler](database/database_handler.py) class which will sort out your database
connection and session for you.
Provided a database URL in the [.env](.env.example) file, the bot will initialise the handler and create tables based on
entity models you define.

An example model is included in [entities/example_entity.py](entities/example_entity.py).

The bot automatically commits changes to the database every 6 hours and on bot shutdown, though realistically SQLAlchemy
should already handle things pretty well.

### Extension loading

The bot is able to load extensions (holding cogs) from a specified directory - by default, the `extensions` directory.
This allows you to keep your codebase clean and modular, and to easily add or remove functionality.

In the template, the [BaseCog](base/base_cog.py) class is provided as a base class for your cogs. It includes a logger,
reference to the bot, and a post-initialisation method which you can override to perform any setup tasks that should
happen after other cogs and the database have been initialised.

### Logging system

A flexible logging system is included, making use of Python's built-in logging module. By default, the bot itself as
well as all cogs have a logger object that appends their name to the log messages for easy debugging.

Additionally, a get_logger_for method is provided to allow you to get a logger for any class or function. This allows
for even more granular logging, and is especially useful for debugging.

By default, the bot logs to the console and to a rotating file handler, which will keep the last 5 log files.

### (Attempt at) sensible architecture

The template is structured in a way that should make it easy to understand and extend. It uses a flat package structure
with a hopefully clear separation of concerns. Outside of the example entity, the template does not include any
functionality that you (most likely) might not need.

### Provided extensions

The template includes a few basic extensions that I use in most of my bots. These include:

- core: Contains core functionality and commands, such as a sync command to sync your command tree, a ping command, a
  shutdown command, and a command with autocomplete that generates a link for any command.
- error: Contains an error handler that logs errors and sends a message to the user if a command raises an error. If the
  bot owner triggers an error, the error message is DM'd to them for easier debugging.
- command_logging: Very simple cog that logs command usage. Depending on the size of your userbase and frequency of
  commands, you may want to consider disabling/removing this.

## Support

If you need help with the template, have a feature request, or found a bug, feel free to open an issue on the GitHub
repository. I'll do my best to help you out. For more general questions or discussions, you can join my
[Discord server](https://discord.gg/8PJeFeMCsu). If you have questions related to the discord.py library, they have an
excellent [Discord server](https://discord.gg/r3sSKJJ) as well.

This template is provided as-is, and I cannot guarantee that it is 100% bug-free. Always test your changes before
deploying them to a live bot.