from aiogram import types


def get_reply_keyboard(buttons: list[list[str]]) -> types.ReplyKeyboardMarkup:
    keyboard = [[types.KeyboardButton(text=j) for j in i] for i in buttons]

    return types.ReplyKeyboardMarkup(
        keyboard=keyboard, resize_keyboard=True
    )


def get_inline_keyboard(buttons: list[list[dict[str:str]]]) -> types.InlineKeyboardMarkup:
    keyboard = [
        [list(map(lambda o: types.InlineKeyboardButton(text=o, callback_data=j[o]), j))[0] for j in i] for i in buttons
    ]

    return types.InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
