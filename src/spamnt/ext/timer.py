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

    def __post_init__(self):
        self.delete: dict[int, bool] = {}

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
        if not message.author.bot:
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



