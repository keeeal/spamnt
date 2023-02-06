import logging
from asyncio import Task, create_task, sleep
from dataclasses import dataclass
from typing import Optional

from discord import Message, Reaction, User
from discord.ext.commands import Bot, Cog


@dataclass
class Timer(Cog):
    bot: Bot
    delay: int
    bot_ids: list[int]
    ignore_channel_ids: Optional[list[int]] = None

    def __post_init__(self):
        self.tasks: dict[int, Task] = {}

    def valid_message(self, message: Message) -> bool:
        if not message.author.bot:
            return False

        if not message.author.id in self.bot_ids:
            return False

        if self.ignore_channel_ids:
            if message.channel.id in self.ignore_channel_ids:
                return False

        return True

    def valid_reaction(self, reaction: Reaction, user: User) -> bool:
        if user.bot:
            return False

        if reaction.message.id not in self.tasks:
            return False

        return True

    async def delete(self, message: Message) -> None:
        await sleep(self.delay)
        logging.info(f"Deleting message {message.id}")
        del self.tasks[message.id]
        await message.delete()

    @Cog.listener()
    async def on_message(self, message: Message):
        if not self.valid_message(message):
            return

        logging.info(f"Watching message {message.id}")
        self.tasks[message.id] = create_task(self.delete(message))

    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: User):
        if not self.valid_reaction(reaction, user):
            return

        logging.info(f"Pinning message {reaction.message.id}")
        self.tasks[reaction.message.id].cancel()

    @Cog.listener()
    async def on_reaction_remove(self, reaction: Reaction, user: User):
        if not self.valid_reaction(reaction, user):
            return

        if not all(
            [
                user.bot
                for reaction in reaction.message.reactions
                async for user in reaction.users()
            ]
        ):
            return

        logging.info(f"Unpinning message {reaction.message.id}")
        self.tasks[reaction.message.id] = create_task(self.delete(reaction.message))
