import math
import uuid
from enum import Enum

from aiogram import F, Router, types
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nespresso.bot.lib.messaging.checks import CheckVerified
from nespresso.bot.lib.messaging.stream import (
    MsgContext,
    ReceiveCallback,
    ReceiveMessage,
    SendMessage,
)
from nespresso.recsys.preprocessing.embedding import CalculateTokenLen
from nespresso.recsys.preprocessing.model import TOKEN_LEN
from nespresso.recsys.searching.search import SEARCHES, Page, ScrollingSearch

router = Router()


def PrecentageToReduce(text: str) -> int:
    length = CalculateTokenLen(text)

    return math.ceil((length - TOKEN_LEN) / length * 10) * 10


class FindAction(str, Enum):
    Prev = "previous"
    Next = "next"


class FindCallbackData(CallbackData, prefix="find"):
    action: FindAction
    search_id: uuid.UUID


def MarkupKeyboard(
    search_id: uuid.UUID,
    prev: bool = False,
    next: bool = False,
) -> InlineKeyboardMarkup | None:
    def Button(action: FindAction) -> InlineKeyboardButton:
        nonlocal search_id

        callback_data = FindCallbackData(action=action, search_id=search_id).pack()

        return InlineKeyboardButton(
            text="⬅️" if action is FindAction.Prev else "➡️",
            callback_data=callback_data,
        )

    buttons: list[InlineKeyboardButton] = []

    if prev:
        buttons.append(Button(FindAction.Prev))
    if next:
        buttons.append(Button(FindAction.Next))

    if not buttons:
        return None

    return InlineKeyboardMarkup(inline_keyboard=[buttons])


class FindStates(StatesGroup):
    Text = State()
    Forward = State()


@router.message(StateFilter(None), Command("find"))
async def CommandFind(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    if not await CheckVerified(chat_id=message.chat.id):
        await SendMessage(
            chat_id=message.chat.id,
            text="Only registered users can use /find",
        )
        return

    await SendMessage(
        chat_id=message.chat.id,
        text="Type text for query of person you wish to find",
    )
    await state.set_state(FindStates.Text)


@router.message(StateFilter(FindStates.Text), F.content_type == "text")
async def CommandFindText(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)
    assert message.text is not None

    if CalculateTokenLen(message.text) > TOKEN_LEN:
        await SendMessage(
            chat_id=message.chat.id,
            text=f"Your text is too long.\nPlease, reduce it by {PrecentageToReduce(message.text)}%",
            context=MsgContext.UserFailed,
        )
        return

    await SendMessage(
        chat_id=message.chat.id,
        text="Doing search.\nPlease, wait",
    )

    search = ScrollingSearch()
    page = await search.HybridSearch(message)

    if page is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="Found nothing",
        )
        await state.clear()
        return

    search_id = uuid.uuid4()
    SEARCHES[search_id] = search

    await SendMessage(
        chat_id=message.chat.id,
        text=page.GetFormattedText(),
        reply_markup=MarkupKeyboard(search_id=search_id, next=True),
    )

    await state.clear()


@router.callback_query(FindCallbackData.filter())
async def CommandFindCallback(
    callback_query: types.CallbackQuery,
    callback_data: FindCallbackData,
) -> None:
    await ReceiveCallback(callback_query, callback_data)
    assert isinstance(callback_query.message, types.Message)

    search_id = callback_data.search_id
    search: ScrollingSearch | None = SEARCHES.get(search_id, None)

    if search is None:
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer("Search is expired")

        return

    page: Page | None
    if callback_data.action == FindAction.Prev:
        page = await search.ScrollBackward()
    else:
        page = await search.ScrollForward()

        if page is None:
            await callback_query.message.edit_reply_markup(
                reply_markup=MarkupKeyboard(
                    search_id=search_id,
                    prev=search.index > 0,
                )
            )
            await callback_query.answer("No more pages")

            return

    markup = MarkupKeyboard(
        search_id=search_id,
        prev=search.CanScrollFutherBackward(),
        next=search.CanScrollFutherForward(),
    )

    await callback_query.message.edit_text(
        text=page.GetFormattedText(),
        reply_markup=markup,
    )
    await callback_query.answer()
