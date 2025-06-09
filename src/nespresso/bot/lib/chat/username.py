import logging

from nespresso.bot.lifecycle.creator import bot


async def GetChatTgUsername(chat_id: int) -> str | None:
    try:
        chat = await bot.get_chat(chat_id)
        return chat.username

    except Exception as e:
        logging.warning(f"Failed to get chat info for chat_id={chat_id}: {e}")
        return None
