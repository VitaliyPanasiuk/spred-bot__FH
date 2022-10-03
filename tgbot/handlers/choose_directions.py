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

from tgbot.keyboards.inlineBtn import main_page,user_settings_btn

import datetime
import asyncio
import json

choose_directions_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
cur = base.cursor()

@choose_directions_router.callback_query(lambda c: c.data == 'simple direction')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = user_settings_btn()
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('Найпростіші (Найліквідніші) зв’язки',))
    spread_direction = cur.fetchone()
    cur.execute('''INSERT INTO is_direction_on_for_user (user_id,spread_direction)
        SELECT %s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(user[0],spread_direction[0],user[0]))
    cur.execute('''UPDATE is_direction_on_for_user SET spread_direction = %s
        WHERE
            EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(spread_direction[0],user[0]))
    base.commit()
    
@choose_directions_router.callback_query(lambda c: c.data == 'interexchange')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = user_settings_btn()
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('Міжбіржові',))
    spread_direction = cur.fetchone()
    cur.execute('''INSERT INTO is_direction_on_for_user (user_id,spread_direction)
        SELECT %s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(user[0],spread_direction[0],user[0]))
    cur.execute('''UPDATE is_direction_on_for_user SET spread_direction = %s
        WHERE
            EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(spread_direction[0],user[0]))
    base.commit()
            
@choose_directions_router.callback_query(lambda c: c.data == 'cash')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = user_settings_btn()
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('Готівка',))
    spread_direction = cur.fetchone()
    cur.execute('''INSERT INTO is_direction_on_for_user (user_id,spread_direction)
        SELECT %s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(user[0],spread_direction[0],user[0]))
    cur.execute('''UPDATE is_direction_on_for_user SET spread_direction = %s
        WHERE
            EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(spread_direction[0],user[0]))
    base.commit()
            
@choose_directions_router.callback_query(lambda c: c.data == 'binance')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = user_settings_btn()
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('Binance',))
    spread_direction = cur.fetchone()
    cur.execute('''INSERT INTO is_direction_on_for_user (user_id,spread_direction)
        SELECT %s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(user[0],spread_direction[0],user[0]))
    cur.execute('''UPDATE is_direction_on_for_user SET spread_direction = %s
        WHERE
            EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(spread_direction[0],user[0]))
    base.commit()
            
@choose_directions_router.callback_query(lambda c: c.data == 'okx')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = user_settings_btn()
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('OKX',))
    spread_direction = cur.fetchone()
    cur.execute('''INSERT INTO is_direction_on_for_user (user_id,spread_direction)
        SELECT %s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(user[0],spread_direction[0],user[0]))
    cur.execute('''UPDATE is_direction_on_for_user SET spread_direction = %s
        WHERE
            EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(spread_direction[0],user[0]))
    base.commit()
            
@choose_directions_router.callback_query(lambda c: c.data == 'bybit')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = user_settings_btn()
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('ByBit',))
    spread_direction = cur.fetchone()
    cur.execute('''INSERT INTO is_direction_on_for_user (user_id,spread_direction)
        SELECT %s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(user[0],spread_direction[0],user[0]))
    cur.execute('''UPDATE is_direction_on_for_user SET spread_direction = %s
        WHERE
            EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(spread_direction[0],user[0]))
    base.commit()
            
@choose_directions_router.callback_query(lambda c: c.data == 'wise')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = user_settings_btn()
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('Wise',))
    spread_direction = cur.fetchone()
    cur.execute('''INSERT INTO is_direction_on_for_user (user_id,spread_direction)
        SELECT %s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(user[0],spread_direction[0],user[0]))
    cur.execute('''UPDATE is_direction_on_for_user SET spread_direction = %s
        WHERE
            EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(spread_direction[0],user[0]))
    base.commit()
            
@choose_directions_router.callback_query(lambda c: c.data == 'localbitcoins')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = user_settings_btn()
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('LocalBitcoins',))
    spread_direction = cur.fetchone()
    cur.execute('''INSERT INTO is_direction_on_for_user (user_id,spread_direction)
        SELECT %s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(user[0],spread_direction[0],user[0]))
    cur.execute('''UPDATE is_direction_on_for_user SET spread_direction = %s
        WHERE
            EXISTS (
                SELECT user_id FROM is_direction_on_for_user WHERE user_id = %s
            )''',(spread_direction[0],user[0]))
    base.commit()