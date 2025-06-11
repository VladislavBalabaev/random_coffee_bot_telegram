from nespresso.bot.lib.message.io import ContextIO, SendMessage
from nespresso.bot.lifecycle.creator import bot


async def ProcessPendingUpdates() -> None:
    """
    Notifies users with pending updates when the bot becomes active again.
    Retrieves any pending updates, logs the messages, and prompts users to try again.
    """
    updates = await bot.get_updates(offset=None, timeout=1)

    notified_users = set()

    for update in updates:
        message = update.message

        if message is None:
            continue

        chat_id = message.chat.id

        if chat_id not in notified_users:
            await SendMessage(
                chat_id=chat_id,
                text="Bot has been inactive.\nPlease try again!",
                context=ContextIO.Pending,
            )

            notified_users.add(chat_id)

    await bot.get_updates(offset=updates[-1].update_id + 1 if updates else None)
