from nespresso.bot.lib.message.io import ContextIO, ReceiveMessage, SendMessage
from nespresso.bot.lifecycle.creator import bot


async def ProcessPendingUpdates() -> None:
    """
    Notifies users with pending updates when the bot becomes active again.
    Retrieves any pending updates, logs the messages, and prompts users to try again.
    """
    notified_users = set()

    while True:
        updates = await bot.get_updates(offset=None, timeout=1)

        for update in updates:
            message = update.message

            if message is None:
                continue

            await ReceiveMessage(
                message=message,
                context=ContextIO.Pending,
            )

            if message.chat.id not in notified_users:
                await SendMessage(
                    chat_id=message.chat.id,
                    text="Bot has been inactive.\nPlease try again!",
                    context=ContextIO.Pending,
                )

                notified_users.add(message.chat.id)

        if updates:
            await bot.get_updates(offset=updates[-1].update_id + 1)
        else:
            break
