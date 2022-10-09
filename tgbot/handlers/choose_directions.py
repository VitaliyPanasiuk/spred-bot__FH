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

from tgbot.keyboards.inlineBtn import main_page,user_settings_btn,choose_directions_btn

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
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('Найпростіші (Найліквідніші) зв’язки',))
    spread_direction = cur.fetchone()
    cur.execute('''UPDATE is_direction_on_for_user SET is_on = not is_on
        WHERE user_id = %s and spread_direction = 1
        ''',(user[0],))
    base.commit()
    cur.execute(''' SELECT is_on 
                        FROM is_direction_on_for_user 
                        LEFT JOIN users ON  users.id = is_direction_on_for_user.user_id
                        WHERE telegram_id = %s ORDER BY spread_direction''',(str(user_id),))
    is_on = cur.fetchall()
    btn = choose_directions_btn(is_on)
    await callback_query.message.edit_text('Оберіть напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@choose_directions_router.callback_query(lambda c: c.data == 'interexchange')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('Міжбіржові',))
    spread_direction = cur.fetchone()
    cur.execute('''UPDATE is_direction_on_for_user SET is_on = not is_on
        WHERE user_id = %s and spread_direction = 2
        ''',(user[0],))
    base.commit()
    cur.execute(''' SELECT is_on 
                        FROM is_direction_on_for_user 
                        LEFT JOIN users ON  users.id = is_direction_on_for_user.user_id
                        WHERE telegram_id = %s ORDER BY spread_direction''',(str(user_id),))
    is_on = cur.fetchall()
    btn = choose_directions_btn(is_on)
    await callback_query.message.edit_text('Оберіть напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")
            
@choose_directions_router.callback_query(lambda c: c.data == 'cash')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('Готівка',))
    spread_direction = cur.fetchone()
    cur.execute('''UPDATE is_direction_on_for_user SET is_on = not is_on
        WHERE user_id = %s and spread_direction = 3
        ''',(user[0],))
    base.commit()
    cur.execute(''' SELECT is_on 
                        FROM is_direction_on_for_user 
                        LEFT JOIN users ON  users.id = is_direction_on_for_user.user_id
                        WHERE telegram_id = %s ORDER BY spread_direction''',(str(user_id),))
    is_on = cur.fetchall()
    btn = choose_directions_btn(is_on)
    await callback_query.message.edit_text('Оберіть напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")
            
@choose_directions_router.callback_query(lambda c: c.data == 'binance')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('Binance',))
    spread_direction = cur.fetchone()
    cur.execute('''UPDATE is_direction_on_for_user SET is_on = not is_on
        WHERE user_id = %s and spread_direction = 4
        ''',(user[0],))
    base.commit()
    cur.execute(''' SELECT is_on 
                        FROM is_direction_on_for_user 
                        LEFT JOIN users ON  users.id = is_direction_on_for_user.user_id
                        WHERE telegram_id = %s ORDER BY spread_direction''',(str(user_id),))
    is_on = cur.fetchall()
    btn = choose_directions_btn(is_on)
    await callback_query.message.edit_text('Оберіть напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")
            
@choose_directions_router.callback_query(lambda c: c.data == 'okx')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('OKX',))
    spread_direction = cur.fetchone()
    cur.execute('''UPDATE is_direction_on_for_user SET is_on = not is_on
        WHERE user_id = %s and spread_direction = 5
        ''',(user[0],))
    base.commit()
    cur.execute(''' SELECT is_on 
                        FROM is_direction_on_for_user 
                        LEFT JOIN users ON  users.id = is_direction_on_for_user.user_id
                        WHERE telegram_id = %s ORDER BY spread_direction''',(str(user_id),))
    is_on = cur.fetchall()
    btn = choose_directions_btn(is_on)
    await callback_query.message.edit_text('Оберіть напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")
            
@choose_directions_router.callback_query(lambda c: c.data == 'bybit')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('ByBit',))
    spread_direction = cur.fetchone()
    cur.execute('''UPDATE is_direction_on_for_user SET is_on = not is_on
        WHERE user_id = %s and spread_direction = 6
        ''',(user[0],))
    base.commit()
    cur.execute(''' SELECT is_on 
                        FROM is_direction_on_for_user 
                        LEFT JOIN users ON  users.id = is_direction_on_for_user.user_id
                        WHERE telegram_id = %s ORDER BY spread_direction''',(str(user_id),))
    is_on = cur.fetchall()
    btn = choose_directions_btn(is_on)
    await callback_query.message.edit_text('Оберіть напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")
            
@choose_directions_router.callback_query(lambda c: c.data == 'wise')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('Wise',))
    spread_direction = cur.fetchone()
    cur.execute('''UPDATE is_direction_on_for_user SET is_on = not is_on
        WHERE user_id = %s and spread_direction = 7
        ''',(user[0],))
    base.commit()
    cur.execute(''' SELECT is_on 
                        FROM is_direction_on_for_user 
                        LEFT JOIN users ON  users.id = is_direction_on_for_user.user_id
                        WHERE telegram_id = %s ORDER BY spread_direction''',(str(user_id),))
    is_on = cur.fetchall()
    btn = choose_directions_btn(is_on)
    await callback_query.message.edit_text('Оберіть напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")
            
@choose_directions_router.callback_query(lambda c: c.data == 'localbitcoins')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    cur.execute("SELECT id FROM spread_directions WHERE name = %s",('LocalBitcoins',))
    spread_direction = cur.fetchone()
    cur.execute('''UPDATE is_direction_on_for_user SET is_on = not is_on
        WHERE user_id = %s and spread_direction = 8
        ''',(user[0],))
    base.commit()
    cur.execute(''' SELECT is_on 
                        FROM is_direction_on_for_user 
                        LEFT JOIN users ON  users.id = is_direction_on_for_user.user_id
                        WHERE telegram_id = %s ORDER BY spread_direction''',(str(user_id),))
    is_on = cur.fetchall()
    btn = choose_directions_btn(is_on)
    await callback_query.message.edit_text('Оберіть напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")