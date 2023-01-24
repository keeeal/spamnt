import logging

from discord import Intents
from discord.ext.commands import Bot


class Spamnt(Bot):
    def __init__(self, command_prefix: str):
        intents = Intents.default()
        intents.members = True
        super().__init__(command_prefix, intents=intents)

    async def on_ready(self) -> None:
        logging.info("Bot ready")
