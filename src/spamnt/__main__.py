import logging
from argparse import ArgumentParser
from asyncio import run
from pathlib import Path

from .bot import Spamnt
from .ext.timer import Timer
from .utils.config import read_config

DEFAULT_CONFIG = {
    "secret": {"token": ""},
    "bot": {"command_prefix": "!!!"},
    "timer": {"seconds_to_live": 60, "pin_emoji": "🎺"},
}


def main(config_file: Path):
    logging.basicConfig(level=logging.INFO)
    config = read_config(config_file, DEFAULT_CONFIG)

    if not config["secret"]["token"]:
        logging.error(f"No token in '{config_file}'")
        return

    bot = Spamnt(**config["bot"])

    if "timer" in config:
        run(bot.add_cog(Timer(bot, **config["timer"])))

    bot.run(config["secret"]["token"])


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--config-file", type=Path, default="/config/config.json")
    main(**vars(parser.parse_args()))
