import shelve
import platform
from typing import List
import discord

from stallmansdiscord import config
from stallmansdiscord.client import StallmansClient


def interject(author: str) -> bool:
    with shelve.open("not_gnu_folks.db") as db:
        db[author] = db.get(author, 0) + 1
        if db[author] > config.MEGA_INTERJECTION:
            db[author] = 0
            return True
    return False


@StallmansClient.register_handler(
    "nano", "linux", "emacs", "grep", "windows", "vscode", "visual studio"
)
async def on_gnu(self: StallmansClient, message: discord.Message, matches: List[str]):
    def not_generator(thing):
        return f"Not {thing}, GNU/{thing.title()}"

    if "gnu" not in message.content.lower():
        if interject(str(message.author)):
            await message.channel.send(config.MEGA_INTERJECTION_RANT)

        msg = ". ".join(not_generator(thing) for thing in matches)
        await message.channel.send(f"Guys, please. {msg}")


@StallmansClient.register_handler("stallman", "richard stallman", "rms")
async def on_rms(self: StallmansClient, message: discord.Message, matches: List[str]):
    match = matches.pop()
    if "holy" not in message.content.lower():
        await message.channel.send(f"Guys please. Not {match}, Holy {match}")
    else:
        await message.channel.send(f"God may bless Holy {match}")


@StallmansClient.register_handler("platform")
async def on_platform(
    self: StallmansClient, message: discord.Message, matches: List[str]
):
    plat = platform.system()
    await message.channel.send(f"This bot runs under GNU/{plat}")


if __name__ == "__main__":
    client = StallmansClient()
    client.run(config.DISCORD_TOKEN)
