from enum import Enum

from aiogram import F, Router, types
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.state import StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nespresso.bot.lib.chat.block import BlockUser, CheckIfBlocked, UnblockUser
from nespresso.bot.lib.message.filters import AdminFilter
from nespresso.bot.lib.message.io import ContextIO, SendMessage
from nespresso.db.services.user_context import GetUserContextService

router = Router()


class BlockingAction(str, Enum):
    Block = "Block"
    Unblock = "Unblock"
    Leave = "Leave as is"


class BlockingCallbackData(CallbackData, prefix="blocking"):
    action: BlockingAction
    chat_id: int


def BlockingKeyboard(
    actions: list[BlockingAction], chat_id: int
) -> InlineKeyboardMarkup:
    def Button(action: BlockingAction) -> InlineKeyboardButton:
        nonlocal chat_id

        return InlineKeyboardButton(
            text=action.value,
            callback_data=BlockingCallbackData(action=action, chat_id=chat_id).pack(),
        )

    buttons: list[InlineKeyboardButton] = [Button(a) for a in actions]

    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@router.message(Command("blocking"), StateFilter(None), AdminFilter())
async def CommandBlocking(
    message: types.Message,
    command: CommandObject,
) -> None:
    if not command.args or len(command.args.split()) != 1:
        await SendMessage(
            chat_id=message.chat.id,
            text="Include tg username:\n/blocking @vbalab",
            context=ContextIO.UserFailed,
        )
        return

    ctx = await GetUserContextService()
    chat_id = await ctx.GetTgChatIdBy(tg_username=command.args.replace("@", "").strip())

    if chat_id is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="No such user.",
        )
        return

    blocked = await CheckIfBlocked(chat_id)

    if blocked:
        await SendMessage(
            chat_id=message.chat.id,
            text="🔴 User is blocked.\n\nDo you want to unblock?",
            reply_markup=BlockingKeyboard(
                actions=[BlockingAction.Unblock, BlockingAction.Leave],
                chat_id=chat_id,
            ),
        )
        return

    await SendMessage(
        chat_id=message.chat.id,
        text="🟢 User is not blocked.\n\nDo you want to block?",
        reply_markup=BlockingKeyboard(
            actions=[BlockingAction.Block, BlockingAction.Leave],
            chat_id=chat_id,
        ),
    )


@router.callback_query(BlockingCallbackData.filter(F.action == BlockingAction.Unblock))
async def CommandBlockingUnblock(
    callback_query: types.CallbackQuery,
    callback_data: BlockingCallbackData,
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await UnblockUser(callback_data.chat_id)

    await callback_query.message.edit_text(
        text="🟢 User is not blocked now.",
        reply_markup=None,
    )
    await callback_query.answer()


@router.callback_query(BlockingCallbackData.filter(F.action == BlockingAction.Block))
async def CommandBlockingBlock(
    callback_query: types.CallbackQuery, callback_data: BlockingCallbackData
) -> None:
    assert isinstance(callback_query.message, types.Message)

    await BlockUser(callback_data.chat_id)

    await callback_query.message.edit_text(
        text="🔴 User is blocked now.",
        reply_markup=None,
    )
    await callback_query.answer()


@router.callback_query(BlockingCallbackData.filter(F.action == BlockingAction.Leave))
async def CommandBlockingCancel(callback_query: types.CallbackQuery) -> None:
    assert isinstance(callback_query.message, types.Message)

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer("Cancelled")
