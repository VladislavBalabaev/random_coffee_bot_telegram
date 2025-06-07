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

from nespresso.bot.lib.messaging.filters import VerifiedFilter
from nespresso.bot.lib.messaging.stream import (
    MessageContext,
    ReceiveCallback,
    ReceiveMessage,
    SendMessage,
)
from nespresso.recsys.preprocessing.embedding import CalculateTokenLen
from nespresso.recsys.preprocessing.model import TOKEN_LEN
from nespresso.recsys.searchbase.search import ScrollingSearch, SearchPage

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


class FindKeyboard:
    def __init__(self) -> None:
        self.search_id = uuid.uuid4()

    def _Button(self, action: FindAction) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text="⬅️" if action is FindAction.Prev else "➡️",
            callback_data=FindCallbackData(
                action=action,
                search_id=self.search_id,
            ).pack(),
        )

    def Markup(self, prev: bool = False, next: bool = False) -> InlineKeyboardMarkup:
        buttons: list[InlineKeyboardButton] = []

        if prev:
            buttons.append(self._Button(FindAction.Prev))
        if next:
            buttons.append(self._Button(FindAction.Next))

        return InlineKeyboardMarkup(inline_keyboard=[buttons])


class FindStates(StatesGroup):
    Text = State()
    Forward = State()


# TODO: do actual formatting
def FormatPage(page: SearchPage) -> str:
    assert len(page.items) == 1

    text = f"[Page: {page.number}]\n\n"
    text += f"{page.items[0].text}"

    return text


@router.message(StateFilter(None), Command("find"))
async def CommandFind(message: types.Message, state: FSMContext) -> None:
    await ReceiveMessage(message)

    if not await VerifiedFilter(chat_id=message.chat.id):
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
            context=MessageContext.UserFailed,
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

    keyboard = FindKeyboard()
    search_id = keyboard.search_id

    await SendMessage(
        chat_id=message.chat.id,
        text=FormatPage(page),
        reply_markup=keyboard.Markup(next=True),
    )

    await state.set_state(None)
    await state.update_data(
        {
            f"scrolling_search{search_id}": search,
            f"keyboard{search_id}": keyboard,
        }
    )


@router.callback_query(FindCallbackData.filter())
async def CommandFindCallback(
    callback_query: types.CallbackQuery,
    callback_data: FindCallbackData,
    state: FSMContext,
) -> None:
    await ReceiveCallback(callback_query, callback_data)
    assert isinstance(callback_query.message, types.Message)

    search_id = callback_data.search_id
    data = await state.get_data()

    if f"scrolling_search{search_id}" not in data:
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer("Search is expired")

        return

    search: ScrollingSearch = data[f"scrolling_search{search_id}"]
    keyboard: FindKeyboard = data[f"keyboard{search_id}"]

    page: SearchPage | None
    if callback_data.action == FindAction.Prev:
        page = await search.ScrollBackward()
    else:
        page = await search.ScrollForward()

        if page is None:
            if search.index > 0:
                await callback_query.message.edit_reply_markup(
                    reply_markup=keyboard.Markup(prev=True)
                )
            else:
                await callback_query.message.edit_reply_markup(reply_markup=None)

            await callback_query.answer("No more pages")

            return

    markup = keyboard.Markup(
        prev=search.CanScrollFutherBackward(),
        next=search.CanScrollFutherForward(),
    )

    await callback_query.message.edit_text(
        text=FormatPage(page),
        reply_markup=markup,
    )
    await callback_query.answer()
