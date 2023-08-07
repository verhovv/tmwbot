from bot.adminpanel import AdminPanelAction, AdminPanelCallbackFactory, EditActions, EditUserCallbackFactory
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_find_by_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Искать по никнейму исполнителя', callback_data=AdminPanelCallbackFactory(
            action=AdminPanelAction.find_by_chaturbate_nickname).pack())],
        [InlineKeyboardButton(text='Искать по никнейму модели', callback_data=AdminPanelCallbackFactory(
            action=AdminPanelAction.find_by_model_nickname).pack())]
    ])


def get_edit_user_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Изменить имя исполнителя', callback_data=EditUserCallbackFactory(id=user_id,
                                                                                                     action=EditActions.edit_chaturbate_nickname).pack())],
        [InlineKeyboardButton(text='Изменить имя модели', callback_data=EditUserCallbackFactory(id=user_id,
                                                                                                action=EditActions.edit_model_nickname).pack())],
        [InlineKeyboardButton(text='Изменить баланс', callback_data=EditUserCallbackFactory(id=user_id,
                                                                                            action=EditActions.edit_balance).pack())],
    ])
