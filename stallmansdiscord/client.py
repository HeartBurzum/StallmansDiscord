from collections import defaultdict
import discord


class StallmansClient(discord.Client):
    _callbacks = defaultdict(list)

    def __init__(self):
        intents = discord.Intents.all()
        intents.members = True
        intents.presences = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="out for GNU")
        )

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        content = message.content.lower()
        matches = []
        items_list = []
        for pattern, callback in self._callbacks.items():
            items_list.append([pattern, callback])

        for item in items_list:
            if item[0] in content:
                matches.append(pattern)

        if matches:
            for item in items_list:
                await item[1](self, message, matches)

    @classmethod
    def register_handler(cls, *patterns):
        def wrapper(func):
            cls._callbacks[patterns].append(func)
            return func

        return wrapper
