from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from nespresso.bot.lib.messaging.checks import checker
from nespresso.bot.lib.messaging.stream import SendMessage

router = Router()


@router.message(Command("cancel"))
@checker
async def CommandCancel(message: types.Message, state: FSMContext) -> None:
    """
    Handles the /cancel command, allowing users to cancel ongoing interactions
    and removing any active reply keyboards. It also clears the user's state.
    """
    await SendMessage(
        message.chat.id, "Все отменили!", reply_markup=types.ReplyKeyboardRemove()
    )

    await state.clear()
