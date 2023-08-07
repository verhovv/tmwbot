from aiogram import Router, types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from bot.adminpanel import AdminPanelCallbackFactory, AdminPanelAction, AdminStates, EditActions, \
    EditUserCallbackFactory, EditStates
from bot.config import time_modes
from bot.database.models import Users, Tasks
from bot.filters import AdminsFilter
from bot.inline_keyboards import get_find_by_keyboard, get_edit_user_keyboard
from bot.keyboards import get_inline_keyboard
from bot.save_statistic import save_statistic

router = Router()


@router.message(Text(text='Админ панель'), AdminsFilter())
async def on_admin_panel_message(message: types.Message):
    await message.answer(text='Выберите способ для поиска', reply_markup=get_find_by_keyboard())


@router.callback_query(AdminPanelCallbackFactory.filter())
async def on_admin_panel_callbacks(callback: types.CallbackQuery, callback_data: AdminPanelCallbackFactory,
                                   state: FSMContext):
    if callback_data.action == AdminPanelAction.find_by_chaturbate_nickname:
        await state.set_state(AdminStates.find_by_chaturbate_nickname)
        await callback.message.answer(text='Введите никнейм исполнителя')
    elif callback_data.action == AdminPanelAction.find_by_model_nickname:
        await state.set_state(AdminStates.find_by_model_nickname)
        await callback.message.answer(text='Введите никнейм модели')
    await callback.answer()


@router.message(AdminStates())
async def on_find_by_model_nickname_message(message: types.Message, state: FSMContext, bot: Bot):
    if await state.get_state() == AdminStates.find_by_chaturbate_nickname:
        users = await Users.filter(chaturbate_nickname=message.text)
        if not users:
            await state.clear()
            await message.answer(
                text='Пользователя с таким ником исполнителя не найдено. Нажмите на кнопку "Искать по нику исполнителя" и попробуйте снова')
            return
    else:
        users = await Users.filter(model_nickname=message.text)
        if not users:
            await state.clear()
            await message.answer(
                text='Пользователя с таким ником модели не найдено. Нажмите на кнопку "Искать по нику модели" и попробуйте снова')
            return

    for user in users:
        username = (await bot.get_chat_member(chat_id=user.id, user_id=user.id)).user.username
        await message.answer(
            text=f'<b>ID:</b> {user.id}\n<b>username:</b> {username}\n<b>chaturbate_nickname:</b> {user.chaturbate_nickname}\n<b>model_nickname:</b> {user.model_nickname}\n<b>balance:</b> {user.balance:.2f}',
            reply_markup=get_edit_user_keyboard(user.id)
        )
    await state.clear()


@router.callback_query(EditUserCallbackFactory.filter())
async def on_edit_user_callbacks(callback: types.CallbackQuery, callback_data: EditUserCallbackFactory,
                                 state: FSMContext):
    if callback_data.action == EditActions.edit_chaturbate_nickname:
        await state.set_state(EditStates.edit_chaturbate_nickname)
        await callback.message.answer(text='Введите новый никнейм исполнителя')
    elif callback_data.action == EditActions.edit_model_nickname:
        await state.set_state(EditStates.edit_model_nickname)
        await callback.message.answer(text='Введите новый никнейм модели')
    elif callback_data.action == EditActions.edit_balance:
        await state.set_state(EditStates.edit_balance)
        await callback.message.answer(text='Введите новый баланс')

    await state.set_data(data={'message_id': callback.message.message_id, 'user_id': callback_data.id})
    await callback.answer()


@router.message(EditStates.edit_model_nickname)
async def on_edit_model_nickname_message(message: types.Message, state: FSMContext, bot: Bot):
    sdata = await state.get_data()

    user = await Users.get(id=sdata['user_id'])
    old_model_name = user.model_nickname
    user.model_nickname = message.text
    await user.save()

    username = (await bot.get_chat_member(chat_id=user.id, user_id=user.id)).user.username

    await message.answer(text=f'Имя исполнителя успешно изменено (<s>{old_model_name}</s> -> <b>{message.text}</b>)')
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=sdata['message_id'],
                                text=f'<b>ID:</b> {user.id}\n<b>username:</b> {username}\n<b>chaturbate_nickname:</b> {user.chaturbate_nickname}\n<b>model_nickname:</b> {user.model_nickname}\n<b>balance:</b> {user.balance:.2f}',
                                reply_markup=get_edit_user_keyboard(user.id))

    await state.clear()


@router.message(EditStates.edit_chaturbate_nickname)
async def on_edit_chaturbate_nickname_message(message: types.Message, state: FSMContext, bot: Bot):
    sdata = await state.get_data()

    user = await Users.get(id=sdata['user_id'])
    old_model_name = user.chaturbate_nickname
    user.chaturbate_nickname = message.text
    await user.save()

    username = (await bot.get_chat_member(chat_id=user.id, user_id=user.id)).user.username

    await message.answer(text=f'Имя модели успешно изменен (<s>{old_model_name}</s> -> <b>{message.text}</b>)')
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=sdata['message_id'],
                                text=f'<b>ID:</b> {user.id}\n<b>username:</b> {username}\n<b>chaturbate_nickname:</b> {user.chaturbate_nickname}\n<b>model_nickname:</b> {user.model_nickname}\n<b>balance:</b> {user.balance:.2f}',
                                reply_markup=get_edit_user_keyboard(user.id))
    await state.clear()


@router.message(EditStates.edit_balance)
async def on_edit_balance_message(message: types.Message, state: FSMContext, bot: Bot):
    sdata = await state.get_data()

    try:
        balance = int(message.text)
    except ValueError:
        await message.answer(
            text='Недопустимое значение. Пожалуйста, нажмите кнопку "Изменить баланс" и попробуйте снова')
        await state.clear()
        return

    user = await Users.get(id=sdata['user_id'])
    old_balance = user.balance
    user.balance = balance
    await user.save()

    username = (await bot.get_chat_member(chat_id=user.id, user_id=user.id)).user.username

    await message.answer(text=f'Баланс успешно изменен (<s>{old_balance}</s> -> <b>{message.text}</b>)')
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=sdata['message_id'],
                                text=f'<b>ID:</b> {user.id}\n<b>username:</b> {username}\n<b>chaturbate_nickname:</b> {user.chaturbate_nickname}\n<b>model_nickname:</b> {user.model_nickname}\n<b>balance:</b> {user.balance:.2f}',
                                reply_markup=get_edit_user_keyboard(user.id))
    await state.clear()


@router.message(Text(text='Администрирование заданий'), AdminsFilter())
async def on_admin_tasks_message(message: types.Message, state: FSMContext):
    keyboard = list()
    text = ''

    tasks = await Tasks.filter(active=True)
    if not tasks:
        await message.answer(text='Нет доступных заданий')

    for n, task in enumerate(tasks, 1):
        user = await task.user.get()
        text += f'{n}. Никнейм модели: {user.model_nickname}, количество людей: {task.working}\n'
        keyboard.append([{str(n): f'task_keyboard {task.id}'}])

    await message.answer(text=text, reply_markup=get_inline_keyboard(keyboard))


@router.callback_query(lambda x: x.data.split()[0] == 'task_keyboard')
async def on_admin_tasks_callback(callback: types.CallbackQuery):
    await callback.answer()

    _, task_id = callback.data.split()
    task_id = int(task_id)
    task = await Tasks.get(id=task_id)
    user = await task.user.get()

    await callback.message.answer(
        text=f'Никнейм модели: {user.model_nickname}\nКоличество юзеров на задании: {task.working}',
        reply_markup=get_inline_keyboard([[{'-1': f'minus1 {task.id}'}, {'+1': f'plus1 {task.id}'}]]))


@router.callback_query(lambda x: x.data.split()[0] in ['minus1', 'plus1'])
async def on_minus1_callback(callback: types.CallbackQuery):
    await callback.answer()

    pref, task_id = callback.data.split()
    task_id = int(task_id)

    task = await Tasks.get(id=task_id)
    user = await task.user.get()

    if pref == 'minus1':
        task.working -= 1
    else:
        if task.working == task.max_working:
            await callback.message.answer(text='Достигнуто максимальное значение')
            return
        elif task.working == 9:
            task.started = True
            task.end_time = task.start_time + time_modes[task.time_mode][1]

        task.working += 1

    await task.save()
    await callback.message.edit_text(
        text=f'Никнейм модели: {user.model_nickname}\nКоличество юзеров на задании: {task.working}',
        reply_markup=get_inline_keyboard([[{'-1': f'minus1 {task.id}'}, {'+1': f'plus1 {task.id}'}]]))


@router.message(Text(text='Статистика'), AdminsFilter())
async def on_admin_tasks_message(message: types.Message, bot: Bot):
    await save_statistic(bot)
    await message.answer_document(FSInputFile('статистика.xlsx'))
