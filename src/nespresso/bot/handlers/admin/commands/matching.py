from enum import Enum

from aiogram import F, Router, types
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nespresso.bot.handlers.client.commands.find import FindCallbackData
from nespresso.bot.lib.messaging.filters import AdminFilter
from nespresso.bot.lib.messaging.stream import (
    ReceiveCallback,
    ReceiveMessage,
    SendMessage,
)
from nespresso.recsys.matching.schedule import (
    GetNextMatchingTime,
    PauseMatching,
    ResumeMatching,
)

router = Router()


class MatchingAction(str, Enum):
    Pause = "Pause"
    Resume = "Resume"
    Leave = "Leave as is"


class MatchingCallbackData(CallbackData, prefix="matching"):
    action: MatchingAction


def MatchingKeyboard(actions: list[MatchingAction]) -> InlineKeyboardMarkup:
    def Button(action: MatchingAction) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=action.value,
            callback_data=MatchingCallbackData(action=action).pack(),
        )

    buttons: list[InlineKeyboardButton] = [Button(a) for a in actions]

    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@router.message(Command("matching"), StateFilter(None), AdminFilter())
async def CommandMatching(message: types.Message) -> None:
    await ReceiveMessage(message)

    next_run_time = GetNextMatchingTime()

    if next_run_time is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="🔴 Job is paused.\nNo next run scheduled\n\nDo you want to resume?",
            reply_markup=MatchingKeyboard(
                [MatchingAction.Resume, MatchingAction.Leave]
            ),
        )
        return

    await SendMessage(
        chat_id=message.chat.id,
        text=f"🟢 Job is active.\nNext run at {next_run_time.isoformat()}\n\nDo you want to pause?",
        reply_markup=MatchingKeyboard([MatchingAction.Pause, MatchingAction.Leave]),
    )


@router.callback_query(MatchingCallbackData.filter(F.action == MatchingAction.Resume))
async def CommandMatchingResume(
    callback_query: types.CallbackQuery,
    callback_data: FindCallbackData,
) -> None:
    await ReceiveCallback(callback_query, callback_data)
    assert isinstance(callback_query.message, types.Message)

    ResumeMatching()
    next_run = GetNextMatchingTime()
    assert next_run is not None

    await callback_query.message.edit_text(
        text=f"🟢 Job resumed.\nNext run at {next_run.isoformat()}",
        reply_markup=None,
    )
    await callback_query.answer("Weekly matching resumed")


@router.callback_query(MatchingCallbackData.filter(F.action == MatchingAction.Pause))
async def CommandMatchingPause(
    callback_query: types.CallbackQuery,
    callback_data: FindCallbackData,
) -> None:
    await ReceiveCallback(callback_query, callback_data)
    assert isinstance(callback_query.message, types.Message)

    PauseMatching()

    await callback_query.message.edit_text(
        text="🔴 Job paused",
        reply_markup=None,
    )
    await callback_query.answer("Weekly matching paused")


@router.callback_query(MatchingCallbackData.filter(F.action == MatchingAction.Leave))
async def CommandMatchingCancel(
    callback_query: types.CallbackQuery,
    callback_data: FindCallbackData,
) -> None:
    await ReceiveCallback(callback_query, callback_data)
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer("Cancelled")
