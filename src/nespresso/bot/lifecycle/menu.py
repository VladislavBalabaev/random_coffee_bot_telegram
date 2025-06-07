from aiogram.types import BotCommand

from nespresso.bot.lifecycle.creator import bot


async def SetMenu() -> None:
    commands = [
        BotCommand(command="/start", description="Register"),
        BotCommand(command="/find", description="Find alumni by query"),
        BotCommand(command="/cancel", description="Cancel current state"),
        BotCommand(command="/help", description="Help"),
    ]

    await bot.set_my_commands(commands)
