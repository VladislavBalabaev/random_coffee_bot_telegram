from enum import Enum

from aiogram import types


def CreateReplyKeyboard(
    choices: type[Enum], max_buttons_per_row: int = 3
) -> types.ReplyKeyboardMarkup:
    choices_list = list(choices)

    buttons = [
        [
            types.KeyboardButton(text=choice.name)
            for choice in choices_list[i : i + max_buttons_per_row]
        ]
        for i in range(0, len(choices_list), max_buttons_per_row)
    ]

    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
