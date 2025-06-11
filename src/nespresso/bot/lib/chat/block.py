import logging

from nespresso.db.models.tg_user import TgUser
from nespresso.db.services.user_context import GetUserContextService
from nespresso.recsys.searching.document import DeleteUserOpenSearch


async def CheckIfBlocked(chat_id: int) -> bool:
    ctx = await GetUserContextService()
    blocked = await ctx.GetTgUser(chat_id=chat_id, column=TgUser.blocked)

    if blocked:
        logging.info(f"chat_id={chat_id} messages while being blocked.")

    return blocked or False


async def _UnverifyUser(chat_id: int) -> None:
    ctx = await GetUserContextService()

    await ctx.UpdateTgUser(
        chat_id=chat_id,
        column=TgUser.verified,
        value=False,
    )

    nes_id = await ctx.GetTgUser(chat_id=chat_id, column=TgUser.nes_id)
    if nes_id:
        await DeleteUserOpenSearch(nes_id)

    logging.info(f"chat_id={chat_id} unverified.")


async def BlockUser(chat_id: int) -> None:
    ctx = await GetUserContextService()

    await ctx.UpdateTgUser(
        chat_id=chat_id,
        column=TgUser.blocked,
        value=True,
    )

    await _UnverifyUser(chat_id)

    logging.info(f"chat_id={chat_id} blocked.")


async def UnblockUser(chat_id: int) -> None:
    ctx = await GetUserContextService()

    await ctx.UpdateTgUser(
        chat_id=chat_id,
        column=TgUser.blocked,
        value=False,
    )

    logging.info(f"chat_id={chat_id} unblocked.")


async def UserBlockedBot(chat_id: int) -> None:
    await _UnverifyUser(chat_id)

    logging.info(f"chat_id={chat_id} blocked the bot.")
