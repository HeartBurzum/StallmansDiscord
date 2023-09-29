from collections import defaultdict
from discord import Client, Message, Activity, ActivityType


class StallmansClient(Client):
    _callbacks = defaultdict(list)

    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(
            activity=Activity(type=ActivityType.watching, name="out for GNU")
        )

    async def on_message(self, message: Message):
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
