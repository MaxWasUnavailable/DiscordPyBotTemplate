import argparse

from core.bot import MyBot
from core.config import BotConfig
from utils.logging import init_logging

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the bot.')
    parser.add_argument('--config', type=str, help='The path to the config file.', default='./config.yaml',
                        required=False, nargs='?')
    parser.add_argument('--dotenv', type=str, help='The path to the .env file.', default='./.env', required=False,
                        nargs='?')
    parser.add_argument('--token', type=str, help='The bot token.', default=None, required=False, nargs='?')
    parser.add_argument('--database_url', type=str, help='The database URL.', default=None, required=False, nargs='?')
    parser.add_argument('--debug', help='Whether to run the bot in debug mode.', default=None, required=False,
                        nargs='?', type=bool)
    parser.add_argument('--logs_path', type=str, help='The path to the logs directory.', default=None, required=False,
                        nargs='?')
    parser.add_argument('--extensions_path', type=str, help='The path to the extensions directory.', default=None,
                        required=False, nargs='?')
    parser.add_argument('--extensions', type=str, help='The extensions to load.', default=None, required=False,
                        nargs='*')

    args = parser.parse_args()

    cli_args = dict()
    for key, value in vars(args).items():
        if value is not None:
            cli_args[key] = value

    config = BotConfig.from_hierarchy(cli_args['config'], cli_args['dotenv'], cli_args)

    init_logging(config.logs_path, config.debug)

    bot = MyBot(config)
    bot.run(config.token, log_handler=None) # log_handler=None to prevent double logging
