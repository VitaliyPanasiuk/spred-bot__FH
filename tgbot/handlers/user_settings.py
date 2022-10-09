from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.db import db_update

from tgbot.misc.functions import auf_status
from tgbot.misc.messages import info,spread
from tgbot.misc.states import min_spread_state

from tgbot.keyboards.inlineBtn import main_page, balance_btn,home_btn,user_settings_btn,choose_directions_btn,settings_directions_btn,min_spread_settings_btn

import datetime
import asyncio
import json

user_settings_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
cur = base.cursor()


@user_settings_router.callback_query(lambda c: c.data == 'settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = user_settings_btn()
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

    
@user_settings_router.callback_query(lambda c: c.data == 'choose directions')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute(''' SELECT is_on 
                        FROM is_direction_on_for_user 
                        LEFT JOIN users ON  users.id = is_direction_on_for_user.user_id
                        WHERE telegram_id = %s ORDER BY spread_direction''',(str(user_id),))
    is_on = cur.fetchall()
    btn = choose_directions_btn(is_on)
    await callback_query.message.edit_text('Оберіть напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@user_settings_router.callback_query(lambda c: c.data == 'settings directions')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_directions_btn()
    await callback_query.message.edit_text('Налаштувати напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@user_settings_router.callback_query(lambda c: c.data == 'minimal spread')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    # test = callback_query.message.reply_markup.inline_keyboard
    # print(test)
    btn = min_spread_settings_btn()
    await callback_query.message.edit_text('Налаштувати спред',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@user_settings_router.callback_query(lambda c: c.data == 'simple direction spread')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute(''' SELECT ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                        WHERE telegram_id = %s and spread_direction = 1''',(str(user_id),))
    user = cur.fetchone()
    print(user[0])
    btn = home_btn()
    await callback_query.message.edit_text(f'''📏 Налаштування мінімального спреду:
    🔥Найпростіші (Найліквідніші) зв’язки

    Вам будут надходити звіти спредів,
    значення котріх буде вище або
    дорівнювати вашому мінімальному спреду.

    Поточний мінімальний спред: {user[0] if user[0] else "спреди не налаштовані"}

    ❗️ Спред може бути від 0.2% до 100%
    ❗️ Тільки числа
    Введіть нове значення, щоб змінити ваш мінімальний спред''',reply_markup=btn.as_markup(),parse_mode="HTML")
    await state.update_data(id=callback_query.message.message_id)
    await state.update_data(direction='Найпростіші (Найліквідніші) зв’язки')
    await state.set_state(min_spread_state.num)

@user_settings_router.callback_query(lambda c: c.data == 'interexchange spread')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute(''' SELECT ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                        WHERE telegram_id = %s and spread_direction = 2''',(str(user_id),))
    user = cur.fetchone()
    print(user[0])
    btn = home_btn()
    await callback_query.message.edit_text(f'''📏 Налаштування мінімального спреду:
    🔥Міжбіржові

    Вам будут надходити звіти спредів,
    значення котріх буде вище або
    дорівнювати вашому мінімальному спреду.

    Поточний мінімальний спред: {user[0] if user[0] else "спреди не налаштовані"}

    ❗️ Спред може бути від 0.2% до 100%
    ❗️ Тільки числа
    Введіть нове значення, щоб змінити ваш мінімальний спред''',reply_markup=btn.as_markup(),parse_mode="HTML")
    await state.update_data(id=callback_query.message.message_id)
    await state.update_data(direction='Міжбіржові')
    await state.set_state(min_spread_state.num)

@user_settings_router.callback_query(lambda c: c.data == 'cash spread')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute(''' SELECT ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                        WHERE telegram_id = %s and spread_direction = 3''',(str(user_id),))
    user = cur.fetchone()
    print(user[0])
    btn = home_btn()
    await callback_query.message.edit_text(f'''📏 Налаштування мінімального спреду:
    🔥Готівка

    Вам будут надходити звіти спредів,
    значення котріх буде вище або
    дорівнювати вашому мінімальному спреду.

    Поточний мінімальний спред: {user[0] if user[0] else "спреди не налаштовані"}

    ❗️ Спред може бути від 0.2% до 100%
    ❗️ Тільки числа
    Введіть нове значення, щоб змінити ваш мінімальний спред''',reply_markup=btn.as_markup(),parse_mode="HTML")
    await state.update_data(id=callback_query.message.message_id)
    await state.update_data(direction='Готівка')
    await state.set_state(min_spread_state.num)

@user_settings_router.callback_query(lambda c: c.data == 'binance spread')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute(''' SELECT ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                        WHERE telegram_id = %s and spread_direction = 4''',(str(user_id),))
    user = cur.fetchone()
    print(user[0])
    btn = home_btn()
    await callback_query.message.edit_text(f'''📏 Налаштування мінімального спреду:
    🔥Binance

    Вам будут надходити звіти спредів,
    значення котріх буде вище або
    дорівнювати вашому мінімальному спреду.

    Поточний мінімальний спред: {user[0] if user[0] else "спреди не налаштовані"}

    ❗️ Спред може бути від 0.2% до 100%
    ❗️ Тільки числа
    Введіть нове значення, щоб змінити ваш мінімальний спредд''',reply_markup=btn.as_markup(),parse_mode="HTML")
    await state.update_data(id=callback_query.message.message_id)
    await state.update_data(direction='Binance')
    await state.set_state(min_spread_state.num)

@user_settings_router.callback_query(lambda c: c.data == 'okx spread')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute(''' SELECT ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                        WHERE telegram_id = %s and spread_direction = 5''',(str(user_id),))
    user = cur.fetchone()
    print(user[0])
    btn = home_btn()
    await callback_query.message.edit_text(f'''📏 Налаштування мінімального спреду:
    🔥OKX

    Вам будут надходити звіти спредів,
    значення котріх буде вище або
    дорівнювати вашому мінімальному спреду.

    Поточний мінімальний спред: {user[0] if user[0] else "спреди не налаштовані"}

    ❗️ Спред може бути від 0.2% до 100%
    ❗️ Тільки числа
    Введіть нове значення, щоб змінити ваш мінімальний спред''',reply_markup=btn.as_markup(),parse_mode="HTML")
    await state.update_data(id=callback_query.message.message_id)
    await state.update_data(direction='OKX')
    await state.set_state(min_spread_state.num)

@user_settings_router.callback_query(lambda c: c.data == 'bybit spread')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute(''' SELECT ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                        WHERE telegram_id = %s and spread_direction = 6''',(str(user_id),))
    user = cur.fetchone()
    print(user[0])
    btn = home_btn()
    await callback_query.message.edit_text(f'''📏 Налаштування мінімального спреду:
    🔥ByBit

    Вам будут надходити звіти спредів,
    значення котріх буде вище або
    дорівнювати вашому мінімальному спреду.

    Поточний мінімальний спред: {user[0] if user[0] else "спреди не налаштовані"}

    ❗️ Спред може бути від 0.2% до 100%
    ❗️ Тільки числа
    Введіть нове значення, щоб змінити ваш мінімальний спред''',reply_markup=btn.as_markup(),parse_mode="HTML")
    await state.update_data(id=callback_query.message.message_id)
    await state.update_data(direction='ByBit')
    await state.set_state(min_spread_state.num)

@user_settings_router.callback_query(lambda c: c.data == 'wise spread')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute(''' SELECT ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                        WHERE telegram_id = %s and spread_direction = 7''',(str(user_id),))
    user = cur.fetchone()
    print(user[0])
    btn = home_btn()
    await callback_query.message.edit_text(f'''📏 Налаштування мінімального спреду:
    🔥Wise

    Вам будут надходити звіти спредів,
    значення котріх буде вище або
    дорівнювати вашому мінімальному спреду.

    Поточний мінімальний спред: {user[0] if user[0] else "спреди не налаштовані"}

    ❗️ Спред може бути від 0.2% до 100%
    ❗️ Тільки числа
    Введіть нове значення, щоб змінити ваш мінімальний спред''',reply_markup=btn.as_markup(),parse_mode="HTML")
    await state.update_data(id=callback_query.message.message_id)
    await state.update_data(direction='Wise')
    await state.set_state(min_spread_state.num)

@user_settings_router.callback_query(lambda c: c.data == 'localbitcoins spread')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute(''' SELECT ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                        WHERE telegram_id = %s and spread_direction = 8''',(str(user_id),))
    user = cur.fetchone()
    print(user[0])
    btn = home_btn()
    await callback_query.message.edit_text(f'''📏 Налаштування мінімального спреду:
    🔥LocalBitcoins

    Вам будут надходити звіти спредів,
    значення котріх буде вище або
    дорівнювати вашому мінімальному спреду.

    Поточний мінімальний спред: {user[0] if user[0] else "спреди не налаштовані"}

    ❗️ Спред може бути від 0.2% до 100%
    ❗️ Тільки числа
    Введіть нове значення, щоб змінити ваш мінімальний спред''',reply_markup=btn.as_markup(),parse_mode="HTML")
    await state.update_data(id=callback_query.message.message_id)
    await state.update_data(direction='LocalBitcoins')
    await state.set_state(min_spread_state.num)
    
@user_settings_router.message_handler(content_types=types.ContentType.TEXT, state=min_spread_state.num)
async def typeOfOrder(message: types.Message, state: min_spread_state):
    user_id = message.from_user.id
    text = message.text
    if type(text) == int or float:
        await state.update_data(num=text)
        data = await state.get_data()
        cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
        user = cur.fetchone()
        cur.execute("SELECT id FROM spread_directions WHERE name = %s",(data['direction'],))
        direction = cur.fetchone()
        if data['direction'] == 'Найпростіші (Найліквідніші) зв’язки':
            sp_num = 1
        if data['direction'] == 'Міжбіржові':
            sp_num = 2
        if data['direction'] == 'Готівка':
            sp_num = 3
        if data['direction'] == 'Binance':
            sp_num = 4
        if data['direction'] == 'OKX':
            sp_num = 5
        if data['direction'] == 'ByBit':
            sp_num = 6
        if data['direction'] == 'Wise':
            sp_num = 7
        if data['direction'] == 'LocalBitcoins':
            sp_num = 8
        cur.execute("UPDATE minimal_spread SET spread_value = %s WHERE user_id = %s and spread_direction = %s",(data['num'],user[0],sp_num))
        base.commit()
        
        cur.execute(''' SELECT ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                        WHERE telegram_id = %s and spread_direction = %s''',(str(user_id),sp_num))
        user = cur.fetchone()
        btn = home_btn()
        await bot.edit_message_text(chat_id = message.chat.id ,message_id=data['id'], text = f'''📏 Налаштування мінімального спреду:
    🔥{data['direction']}

    Вам будут надходити звіти спредів,
    значення котріх буде вище або
    дорівнювати вашому мінімальному спреду.

    Поточний мінімальний спред: {user[0] if user[0] else "спреди не налаштовані"}

    ❗️ Спред може бути від 0.2% до 100%
    ❗️ Тільки числа
    Введіть нове значення, щоб змінити ваш мінімальний спред''' ,reply_markup=btn.as_markup(),parse_mode="HTML")
        await message.delete()
        await state.set_state(min_spread_state.num)
    else:
        await message.delete()
        await bot.send_message(user_id,'Не правильный формат записи(Только число)')
        await asyncio.sleep(5)
        await bot.delete_message(chat_id = message.chat.id ,message_id = message.message_id + 1 )
        await state.set_state(min_spread_state.num)
    
    
    
    
    
    