import json
import os
from typing import Any

from aiogram import types

from nespresso.bot.lib.messaging.stream import SendDocument
from nespresso.core.configs.paths import DIR_TEMP


def ToJSONText(structure: dict[Any, Any] | list[dict[Any, Any]]) -> str:
    messages_json = json.dumps(structure, indent=3, ensure_ascii=False, default=str)
    messages_formatted = f"<pre>{messages_json}</pre>"

    return messages_formatted


async def SendTemporaryFileFromText(chat_id: int, text: str) -> None:
    file_path = DIR_TEMP / f"chat_id_{chat_id}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

    await SendDocument(chat_id=chat_id, document=types.FSInputFile(file_path))

    os.remove(file_path)
