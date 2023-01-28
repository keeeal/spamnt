import logging
from asyncio import sleep
from dataclasses import dataclass

from discord import Message, Reaction, User
from discord.ext.commands import Bot, Cog


@dataclass
class Timer(Cog):
    bot: Bot
    seconds_to_live: int
    pin_emoji: str
    bot_ids: list[int]
    ignore_channel_ids: list[int]

    def __post_init__(self):
        self.delete: dict[int, bool] = {}

    def valid_message(self, message: Message) -> bool:
        if not message.author.bot:
            return False

        if not message.author.id in self.bot_ids:
            return False

        if message.channel.id in self.ignore_channel_ids:
            return False

        return True

    def valid_reaction(self, reaction: Reaction, user: User) -> bool:
        if user.bot:
            return False

        if reaction.emoji != self.pin_emoji:
            return False

        if reaction.message.id not in self.delete:
            return False

        return True

    @Cog.listener()
    async def on_message(self, message: Message):
        if not self.valid_message(message):
            return

        logging.info(f"Watching message {message.id}")
        self.delete[message.id] = True
        await sleep(self.seconds_to_live)

        if self.delete.get(message.id):
            logging.info(f"Deleting message {message.id}")
            await message.delete()

        del self.delete[message.id]

    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: User):
        if not self.valid_reaction(reaction, user):
            return

        logging.info(f"Pinning message {reaction.message.id}")
        self.delete[reaction.message.id] = False

    @Cog.listener()
    async def on_reaction_remove(self, reaction: Reaction, user: User):
        if not self.valid_reaction(reaction, user):
            return

        logging.info(f"Unpinning message {reaction.message.id}")
        if all([user.bot async for user in reaction.users()]):
            self.delete[reaction.message.id] = True
