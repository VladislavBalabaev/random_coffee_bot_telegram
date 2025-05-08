from aiogram import Dispatcher

from nespresso.bot.handlers.common.commands import cancel, zero


def RegisterHandlerCancel(dp: Dispatcher) -> None:
    """
    Registers the handler for the /cancel command, allowing users to cancel ongoing operations.
    """
    dp.include_routers(
        cancel.router,
    )


def RegisterHandlerZeroMessage(dp: Dispatcher) -> None:
    """
    Registers the handler for cases when no specific command or message is recognized.
    """
    dp.include_routers(
        zero.router,
    )
