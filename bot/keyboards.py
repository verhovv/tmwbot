from aiogram import types


def get_reply_keyboard(buttons: list[list[str]]) -> types.ReplyKeyboardMarkup:
    keyboard = [[types.KeyboardButton(text=j) for j in i] for i in buttons]

    return types.ReplyKeyboardMarkup(
        keyboard=keyboard, resize_keyboard=True
    )
