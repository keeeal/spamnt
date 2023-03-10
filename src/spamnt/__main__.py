import logging
from argparse import ArgumentParser
from asyncio import run
from pathlib import Path

from .bot import Spamnt
from .ext.timer import Timer
from .utils.config import read_config

DEFAULT_CONFIG = {
    "token": "",
    "bot": {"command_prefix": "!!!"},
    "timer": {"delay": 60, "bot_ids": []},
}


def main(config_file: Path):
    logging.basicConfig(level=logging.INFO)
    config = read_config(config_file, DEFAULT_CONFIG)

    if not config["token"]:
        logging.error(f"No token in '{config_file}'")
        return

    bot = Spamnt(**config["bot"])

    if "timer" in config:
        run(bot.add_cog(Timer(bot, **config["timer"])))

    bot.run(config["token"])


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--config-file", type=Path, default="/config/config.yaml")
    main(**vars(parser.parse_args()))
