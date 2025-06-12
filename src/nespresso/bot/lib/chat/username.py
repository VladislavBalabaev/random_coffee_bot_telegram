import logging

from nespresso.bot.lifecycle.creator import bot
from nespresso.db.models.tg_user import TgUser
from nespresso.db.services.user_context import GetUserContextService


async def GetTgUsername(chat_id: int) -> str | None:
    try:
        chat = await bot.get_chat(chat_id)
        username = chat.username

        ctx = await GetUserContextService()
        db_username = await ctx.GetTgUser(
            chat_id=chat_id,
            column=TgUser.username,
        )

        if username != db_username:
            await ctx.UpdateTgUser(
                chat_id=chat_id,
                column=TgUser.username,
                value=username,
            )

        return username

    except Exception as e:
        logging.warning(f"Failed to get chat info for chat_id={chat_id}: {e}")
        return None


async def GetChatUserLoggingPart(chat_id: int) -> str:
    username = await GetTgUsername(chat_id) or "-/-"
    username = "(" + username + ")"

    return f"chat_id={chat_id:<10} {username:<25}"
