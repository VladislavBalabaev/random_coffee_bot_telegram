from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.state import StateFilter

from nespresso.bot.lib.message.file import SendTemporaryFileFromText, ToJSONText
from nespresso.bot.lib.message.filters import AdminFilter
from nespresso.bot.lib.message.io import ContextIO, SendMessage
from nespresso.db.services.user_context import user_ctx

router = Router()


@router.message(Command("messages"), StateFilter(None), AdminFilter())
async def CommandMessages(message: types.Message, command: CommandObject) -> None:
    if not command.args or len(command.args.split()) != 2:  # noqa: PLR2004
        await SendMessage(
            chat_id=message.chat.id,
            text="Include tg username and limit:\n/messages @vbalab 15",
            context=ContextIO.UserFailed,
        )
        return

    tg_username, limit = command.args.split()

    ctx = await user_ctx()
    chat_id = await ctx.GetTgChatIdBy(tg_username=tg_username.replace("@", ""))

    if chat_id is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="User with such credentials doesn't exist.\nAborting",
            context=ContextIO.UserFailed,
        )
        return

    if not limit.isdigit():
        await SendMessage(
            chat_id=message.chat.id,
            text="Limit should be a number, e.g. 50\nTry again",
            context=ContextIO.UserFailed,
        )
        return

    messages = await ctx.GetRecentMessages(chat_id=chat_id, limit=int(limit))
    messages_dict = [m.IntoDict() for m in messages]
    messages_str = ToJSONText(messages_dict)

    await SendTemporaryFileFromText(chat_id=message.chat.id, text=messages_str)
