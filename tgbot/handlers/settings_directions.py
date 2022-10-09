from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.db import db_update

from tgbot.misc.functions import auf_status,get_settings_directions

from tgbot.keyboards.inlineBtn import main_page,user_settings_btn,settings_simple_direction

import datetime
import asyncio
import json

settings_directions_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
cur = base.cursor()

@settings_directions_router.callback_query(lambda c: c.data == 'simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data == 'interexchange settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_simple_direction(user_id,'interexchange settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data == 'cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data == 'binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data == 'okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data == 'bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data == 'wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data == 'localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
# direction --> simple direction settings
@settings_directions_router.callback_query(lambda c: c.data ==  'settings binance simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_exchanges (user_id,spread_direction,exchange_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    base.commit()
    cur.execute("SELECT exchange_chosen FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1",(user[0],))
    exchange_chosen = cur.fetchone()
    
    if 'Binance' not in exchange_chosen[0]:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = exchange_chosen || ARRAY['Binance']
            WHERE
                (user_id = %s and spread_direction = 1) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = array_remove(exchange_chosen, 'Binance')
            WHERE
                (user_id = %s and spread_direction = 1) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings bybit simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_exchanges (user_id,spread_direction,exchange_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    
    cur.execute("SELECT exchange_chosen FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1",(user[0],))
    exchange_chosen = cur.fetchone()
    
    if 'ByBit' not in exchange_chosen[0]:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = exchange_chosen || ARRAY['ByBit']
            WHERE
                (user_id = %s and spread_direction = 1) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = array_remove(exchange_chosen, 'ByBit')
            WHERE
                (user_id = %s and spread_direction = 1) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings okx simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_exchanges (user_id,spread_direction,exchange_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    
    cur.execute("SELECT exchange_chosen FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1",(user[0],))
    exchange_chosen = cur.fetchone()
    
    if 'OKX' not in exchange_chosen[0]:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = exchange_chosen || ARRAY['OKX']
            WHERE
                (user_id = %s and spread_direction = 1) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = array_remove(exchange_chosen, 'OKX')
            WHERE
                (user_id = %s and spread_direction = 1) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 1
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings privatbank simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 1",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'ПриватБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['ПриватБанк']
            WHERE 
            user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'ПриватБанк')
            WHERE 
                user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings monobank simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 1",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'МоноБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['МоноБанк']
            WHERE 
            user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'МоноБанк')
            WHERE 
                user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings sportbank simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 1",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'СпортБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['СпортБанк']
            WHERE 
            user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'СпортБанк')
            WHERE 
                user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings rayfazen simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 1",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Райфайзен'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Райфайзен']
            WHERE 
            user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Райфайзен')
            WHERE 
                user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings pumb simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 1",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Пумб'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Пумб']
            WHERE 
            user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Пумб')
            WHERE 
                user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings izibank simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 1",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'iziБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['iziБанк']
            WHERE 
            user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'iziБанк')
            WHERE 
                user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings abank simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 1",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Абанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Абанк']
            WHERE 
            user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Абанк')
            WHERE 
                user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings usdt simple direction settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
            )''',(user[0],1,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'USDT'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['USDT']
            WHERE 
            user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'USDT')
            WHERE 
                user_id = %s and spread_direction = 1 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'simple direction settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
# direction --> interexchange settings 
@settings_directions_router.callback_query(lambda c: c.data ==  'settings binance interexchange settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_exchanges (user_id,spread_direction,exchange_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2
            )''',(user[0],2,[],user[0]))
    base.commit()
    cur.execute("SELECT exchange_chosen FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2",(user[0],))
    exchange_chosen = cur.fetchone()
    
    if 'Binance' not in exchange_chosen[0]:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = exchange_chosen || ARRAY['Binance']
            WHERE
                (user_id = %s and spread_direction = 2) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = array_remove(exchange_chosen, 'Binance')
            WHERE
                (user_id = %s and spread_direction = 2) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'interexchange settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings bybit interexchange settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_exchanges (user_id,spread_direction,exchange_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2
            )''',(user[0],2,[],user[0]))
    
    cur.execute("SELECT exchange_chosen FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2",(user[0],))
    exchange_chosen = cur.fetchone()
    
    if 'ByBit' not in exchange_chosen[0]:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = exchange_chosen || ARRAY['ByBit']
            WHERE
                (user_id = %s and spread_direction = 2) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = array_remove(exchange_chosen, 'ByBit')
            WHERE
                (user_id = %s and spread_direction = 2) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'interexchange settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings okx interexchange settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_exchanges (user_id,spread_direction,exchange_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2
            )''',(user[0],2,[],user[0]))
    
    cur.execute("SELECT exchange_chosen FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2",(user[0],))
    exchange_chosen = cur.fetchone()
    
    if 'OKX' not in exchange_chosen[0]:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = exchange_chosen || ARRAY['OKX']
            WHERE
                (user_id = %s and spread_direction = 2) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = array_remove(exchange_chosen, 'OKX')
            WHERE
                (user_id = %s and spread_direction = 2) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 2
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'interexchange settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings privatbank interexchange settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
            )''',(user[0],2,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 2",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'ПриватБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['ПриватБанк']
            WHERE 
            user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'ПриватБанк')
            WHERE 
                user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'interexchange settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings monobank interexchange settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
            )''',(user[0],2,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 2",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'МоноБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['МоноБанк']
            WHERE 
            user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'МоноБанк')
            WHERE 
                user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'interexchange settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings sportbank interexchange settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
            )''',(user[0],2,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 2",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'СпортБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['СпортБанк']
            WHERE 
            user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'СпортБанк')
            WHERE 
                user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'interexchange settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings pumb interexchange settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
            )''',(user[0],2,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 2",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Пумб'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Пумб']
            WHERE 
            user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Пумб')
            WHERE 
                user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'interexchange settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings abank interexchange settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
            )''',(user[0],2,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 2",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Абанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Абанк']
            WHERE 
            user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Абанк')
            WHERE 
                user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'interexchange settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings usdt interexchange settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 2
            )''',(user[0],2,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 2",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'USDT'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['USDT']
            WHERE 
            user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 2
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'USDT')
            WHERE 
                user_id = %s and spread_direction = 2 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'interexchange settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
# direction --> cash settings 
@settings_directions_router.callback_query(lambda c: c.data ==  'settings binance cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_exchanges (user_id,spread_direction,exchange_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3
            )''',(user[0],3,[],user[0]))
    base.commit()
    cur.execute("SELECT exchange_chosen FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3",(user[0],))
    exchange_chosen = cur.fetchone()
    
    if 'Binance' not in exchange_chosen[0]:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = exchange_chosen || ARRAY['Binance']
            WHERE
                (user_id = %s and spread_direction = 3) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = array_remove(exchange_chosen, 'Binance')
            WHERE
                (user_id = %s and spread_direction = 3) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings bybit cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_exchanges (user_id,spread_direction,exchange_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3
            )''',(user[0],3,[],user[0]))
    
    cur.execute("SELECT exchange_chosen FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3",(user[0],))
    exchange_chosen = cur.fetchone()
    
    if 'ByBit' not in exchange_chosen[0]:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = exchange_chosen || ARRAY['ByBit']
            WHERE
                (user_id = %s and spread_direction = 3) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = array_remove(exchange_chosen, 'ByBit')
            WHERE
                (user_id = %s and spread_direction = 3) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings okx cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_exchanges (user_id,spread_direction,exchange_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3
            )''',(user[0],3,[],user[0]))
    
    cur.execute("SELECT exchange_chosen FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3",(user[0],))
    exchange_chosen = cur.fetchone()
    
    if 'OKX' not in exchange_chosen[0]:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = exchange_chosen || ARRAY['OKX']
            WHERE
                (user_id = %s and spread_direction = 3) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_exchanges SET exchange_chosen = array_remove(exchange_chosen, 'OKX')
            WHERE
                (user_id = %s and spread_direction = 3) AND
                EXISTS (
                    SELECT user_id FROM user_directions_exchanges WHERE user_id = %s and spread_direction = 3
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings privatbank cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
            )''',(user[0],3,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 3",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'ПриватБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['ПриватБанк']
            WHERE 
            user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'ПриватБанк')
            WHERE 
                user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings monobank cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
            )''',(user[0],3,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 3",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'МоноБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['МоноБанк']
            WHERE 
            user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'МоноБанк')
            WHERE 
                user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings sportbank cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
            )''',(user[0],3,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 3",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'СпортБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['СпортБанк']
            WHERE 
            user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'СпортБанк')
            WHERE 
                user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings pumb cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
            )''',(user[0],3,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 3",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Пумб'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Пумб']
            WHERE 
            user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Пумб')
            WHERE 
                user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings abank cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
            )''',(user[0],3,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 3",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Абанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Абанк']
            WHERE 
            user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Абанк')
            WHERE 
                user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings usdt cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 3
            )''',(user[0],3,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 3",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'USDT'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['USDT']
            WHERE 
            user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'USDT')
            WHERE 
                user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings busd cash settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 3
            )''',(user[0],3,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 3",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BUSD'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BUSD']
            WHERE 
            user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 3
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BUSD')
            WHERE 
                user_id = %s and spread_direction = 3 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'cash settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
# direction --> binance settings 
@settings_directions_router.callback_query(lambda c: c.data ==  'buy-sell crypto binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    cur.execute("SELECT operation_options_chosen FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 4",(user[0],))
    operation_options_chosen = cur.fetchone()
    
    if 'Купуємо крипту, продаємо її' not in operation_options_chosen[0]:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = operation_options_chosen || ARRAY['Купуємо крипту, продаємо її']
            WHERE
                (user_id = %s and spread_direction = 4) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 4
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = array_remove(operation_options_chosen, 'Купуємо крипту, продаємо її')
            WHERE
                (user_id = %s and spread_direction = 4) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 4
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings buy-exchange binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    
    cur.execute("SELECT operation_options_chosen FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 4",(user[0],))
    operation_options_chosen = cur.fetchone()
    
    if 'Купуємо крипту, міняємо на іншу, продаємо як мейкер' not in operation_options_chosen[0]:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = operation_options_chosen || ARRAY['Купуємо крипту, міняємо на іншу, продаємо як мейкер']
            WHERE
                (user_id = %s and spread_direction = 4) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 4
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = array_remove(operation_options_chosen, 'Купуємо крипту, міняємо на іншу, продаємо як мейкер')
            WHERE
                (user_id = %s and spread_direction = 4) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 4
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings privatbank binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 4",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'ПриватБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['ПриватБанк']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'ПриватБанк')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings monobank binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 4",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'МоноБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['МоноБанк']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'МоноБанк')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings sportbank binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 4",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'СпортБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['СпортБанк']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'СпортБанк')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings rayfazen binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 4",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Райфайзен'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Райфайзен']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Райфайзен')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings pumb binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 4",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Пумб'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Пумб']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Пумб')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings izibank binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 4",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'iziБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['iziБанк']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'iziБанк')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings abank binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 4",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Абанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Абанк']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Абанк')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings obank binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 4",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'ОщадБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['ОщадБанк']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'ОщадБанк')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings otpbank binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 4",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'OTPБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['OTPБанк']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'OTPБанк')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings neobank binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 4",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'NEO'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['NEO']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'NEO')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings usdt binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'USDT'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['USDT']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'USDT')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings busd binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'USDT'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BUSD']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BUSD')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings btc binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BTC'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BTC']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BTC')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings bnb binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BNB'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BNB']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BNB')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings eth binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'ETH'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['ETH']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'ETH')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings uah binance settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'UAH'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['UAH']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'UAH')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'binance settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings shib okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
            )''',(user[0],4,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'SHIB'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['SHIB']
            WHERE 
            user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 4
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'SHIB')
            WHERE 
                user_id = %s and spread_direction = 4 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
# direction --> okx settings     
@settings_directions_router.callback_query(lambda c: c.data ==  'settings buy-sell crypto okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 5
            )''',(user[0],5,[],user[0]))
    base.commit()
    cur.execute("SELECT operation_options_chosen FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 5",(user[0],))
    operation_options_chosen = cur.fetchone()
    
    if 'Купуємо крипту, продаємо її' not in operation_options_chosen[0]:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = operation_options_chosen || ARRAY['Купуємо крипту, продаємо її']
            WHERE
                (user_id = %s and spread_direction = 5) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 5
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = array_remove(operation_options_chosen, 'Купуємо крипту, продаємо її')
            WHERE
                (user_id = %s and spread_direction = 5) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 5
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings buy-exchange okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 5
            )''',(user[0],5,[],user[0]))
    
    cur.execute("SELECT operation_options_chosen FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 5",(user[0],))
    operation_options_chosen = cur.fetchone()
    
    if 'Купуємо крипту, міняємо на іншу, продаємо як мейкер' not in operation_options_chosen[0]:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = operation_options_chosen || ARRAY['Купуємо крипту, міняємо на іншу, продаємо як мейкер']
            WHERE
                (user_id = %s and spread_direction = 5) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 5
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = array_remove(operation_options_chosen, 'Купуємо крипту, міняємо на іншу, продаємо як мейкер')
            WHERE
                (user_id = %s and spread_direction = 5) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 5
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings privatbank okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
            )''',(user[0],5,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 5",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'ПриватБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['ПриватБанк']
            WHERE 
            user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'ПриватБанк')
            WHERE 
                user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings monobank okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
            )''',(user[0],5,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 5",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'МоноБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['МоноБанк']
            WHERE 
            user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'МоноБанк')
            WHERE 
                user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings sportbank okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
            )''',(user[0],5,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 5",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'СпортБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['СпортБанк']
            WHERE 
            user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'СпортБанк')
            WHERE 
                user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings pumb okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
            )''',(user[0],5,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 5",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Пумб'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Пумб']
            WHERE 
            user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Пумб')
            WHERE 
                user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings abank okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
            )''',(user[0],5,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 5",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Абанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Абанк']
            WHERE 
            user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Абанк')
            WHERE 
                user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings usdt okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 5
            )''',(user[0],5,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 5",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'USDT'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['USDT']
            WHERE 
            user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'USDT')
            WHERE 
                user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings btc okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 5
            )''',(user[0],5,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 5",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BTC'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BTC']
            WHERE 
            user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BTC')
            WHERE 
                user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings eth okx settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 5
            )''',(user[0],5,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 5",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'ETH'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['ETH']
            WHERE 
            user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 5
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'ETH')
            WHERE 
                user_id = %s and spread_direction = 5 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'okx settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
# direction --> bybit settings     
@settings_directions_router.callback_query(lambda c: c.data ==  'buy-sell crypto bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 6
            )''',(user[0],6,[],user[0]))
    base.commit()
    cur.execute("SELECT operation_options_chosen FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 6",(user[0],))
    operation_options_chosen = cur.fetchone()
    
    if 'Купуємо крипту, продаємо її' not in operation_options_chosen[0]:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = operation_options_chosen || ARRAY['Купуємо крипту, продаємо її']
            WHERE
                (user_id = %s and spread_direction = 6) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 6
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = array_remove(operation_options_chosen, 'Купуємо крипту, продаємо її')
            WHERE
                (user_id = %s and spread_direction = 6) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 6
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings buy-exchange bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 6
            )''',(user[0],6,[],user[0]))
    
    cur.execute("SELECT operation_options_chosen FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 6",(user[0],))
    operation_options_chosen = cur.fetchone()
    
    if 'Купуємо крипту, міняємо на іншу, продаємо як мейкер' not in operation_options_chosen[0]:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = operation_options_chosen || ARRAY['Купуємо крипту, міняємо на іншу, продаємо як мейкер']
            WHERE
                (user_id = %s and spread_direction = 6) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 6
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = array_remove(operation_options_chosen, 'Купуємо крипту, міняємо на іншу, продаємо як мейкер')
            WHERE
                (user_id = %s and spread_direction = 6) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 6
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings privatbank bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
            )''',(user[0],6,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 6",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'ПриватБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['ПриватБанк']
            WHERE 
            user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'ПриватБанк')
            WHERE 
                user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings monobank bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
            )''',(user[0],6,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 6",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'МоноБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['МоноБанк']
            WHERE 
            user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'МоноБанк')
            WHERE 
                user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings sportbank bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
            )''',(user[0],6,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 6",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'СпортБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['СпортБанк']
            WHERE 
            user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'СпортБанк')
            WHERE 
                user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings pumb bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
            )''',(user[0],6,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 6",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Пумб'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Пумб']
            WHERE 
            user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Пумб')
            WHERE 
                user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings abank bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
            )''',(user[0],6,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 6",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Абанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Абанк']
            WHERE 
            user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Абанк')
            WHERE 
                user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings usdt bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 6
            )''',(user[0],6,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 6",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'USDT'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['USDT']
            WHERE 
            user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'USDT')
            WHERE 
                user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings btc bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 6
            )''',(user[0],6,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 6",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BTC'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BTC']
            WHERE 
            user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BTC')
            WHERE 
                user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings eth bybit settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 6
            )''',(user[0],6,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 6",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'ETH'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['ETH']
            WHERE 
            user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 6
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'ETH')
            WHERE 
                user_id = %s and spread_direction = 6 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'bybit settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
# direction --> wise settings     
@settings_directions_router.callback_query(lambda c: c.data ==  'buy-sell crypto wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    cur.execute("SELECT operation_options_chosen FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 7",(user[0],))
    operation_options_chosen = cur.fetchone()
    
    if 'Купуємо крипту та продаємо (одна платіжна система)' not in operation_options_chosen[0]:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = operation_options_chosen || ARRAY['Купуємо крипту та продаємо (одна платіжна система)']
            WHERE
                (user_id = %s and spread_direction = 7) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 7
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = array_remove(operation_options_chosen, 'Купуємо крипту та продаємо (одна платіжна система)')
            WHERE
                (user_id = %s and spread_direction = 7) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 7
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings buy-exchange wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    
    cur.execute("SELECT operation_options_chosen FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 7",(user[0],))
    operation_options_chosen = cur.fetchone()
    
    if 'Купуємо крипту, конвертуємо на іншу та продаємо (одна платіжна система)' not in operation_options_chosen[0]:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = operation_options_chosen || ARRAY['Купуємо крипту, конвертуємо на іншу та продаємо (одна платіжна система)']
            WHERE
                (user_id = %s and spread_direction = 7) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 7
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = array_remove(operation_options_chosen, 'Купуємо крипту, конвертуємо на іншу та продаємо (одна платіжна система)')
            WHERE
                (user_id = %s and spread_direction = 7) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 7
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings usdt wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'USDT'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['USDT']
            WHERE 
            user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'USDT')
            WHERE 
                user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings btc wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BTC'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BTC']
            WHERE 
            user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BTC')
            WHERE 
                user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings eth wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'ETH'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['ETH']
            WHERE 
            user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'ETH')
            WHERE 
                user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings bnb wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BNB'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BNB']
            WHERE 
            user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BNB')
            WHERE 
                user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings busd wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BUSD'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BUSD']
            WHERE 
            user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 7
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BUSD')
            WHERE 
                user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings eur wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_fiat_currency (user_id,spread_direction,fiat_currency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    
    cur.execute("SELECT fiat_currency_chosen FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7",(user[0],))
    fiat_currency_chosen = cur.fetchone()
    
    if 'EUR'not in fiat_currency_chosen[0]:
        cur.execute('''UPDATE user_directions_fiat_currency SET fiat_currency_chosen = fiat_currency_chosen || ARRAY['EUR']
            WHERE 
            user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_fiat_currency SET fiat_currency_chosen = array_remove(fiat_currency_chosen, 'EUR')
            WHERE 
                user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings gbr wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_fiat_currency (user_id,spread_direction,fiat_currency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    
    cur.execute("SELECT fiat_currency_chosen FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7",(user[0],))
    fiat_currency_chosen = cur.fetchone()
    
    if 'GBR'not in fiat_currency_chosen[0]:
        cur.execute('''UPDATE user_directions_fiat_currency SET fiat_currency_chosen = fiat_currency_chosen || ARRAY['GBR']
            WHERE 
            user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_fiat_currency SET fiat_currency_chosen = array_remove(fiat_currency_chosen, 'GBR')
            WHERE 
                user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings pln wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_fiat_currency (user_id,spread_direction,fiat_currency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    
    cur.execute("SELECT fiat_currency_chosen FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7",(user[0],))
    fiat_currency_chosen = cur.fetchone()
    
    if 'PLN'not in fiat_currency_chosen[0]:
        cur.execute('''UPDATE user_directions_fiat_currency SET fiat_currency_chosen = fiat_currency_chosen || ARRAY['PLN']
            WHERE 
            user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_fiat_currency SET fiat_currency_chosen = array_remove(fiat_currency_chosen, 'PLN')
            WHERE 
                user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings usd wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_fiat_currency (user_id,spread_direction,fiat_currency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    
    cur.execute("SELECT fiat_currency_chosen FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7",(user[0],))
    fiat_currency_chosen = cur.fetchone()
    
    if 'USD'not in fiat_currency_chosen[0]:
        cur.execute('''UPDATE user_directions_fiat_currency SET fiat_currency_chosen = fiat_currency_chosen || ARRAY['USD']
            WHERE 
            user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_fiat_currency SET fiat_currency_chosen = array_remove(fiat_currency_chosen, 'USD')
            WHERE 
                user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings uah wise settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_fiat_currency (user_id,spread_direction,fiat_currency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7
            )''',(user[0],7,[],user[0]))
    base.commit()
    
    cur.execute("SELECT fiat_currency_chosen FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7",(user[0],))
    fiat_currency_chosen = cur.fetchone()
    
    if 'UAH'not in fiat_currency_chosen[0]:
        cur.execute('''UPDATE user_directions_fiat_currency SET fiat_currency_chosen = fiat_currency_chosen || ARRAY['UAH']
            WHERE 
            user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 7
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_fiat_currency SET fiat_currency_chosen = array_remove(fiat_currency_chosen, 'UAH')
            WHERE 
                user_id = %s and spread_direction = 7 AND
                EXISTS (
                    SELECT user_id FROM user_directions_fiat_currency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'wise settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
# direction --> localbitcoins settings 
@settings_directions_router.callback_query(lambda c: c.data ==  'buy-sell crypto localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    cur.execute("SELECT operation_options_chosen FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 8",(user[0],))
    operation_options_chosen = cur.fetchone()
    
    if 'Переводимо на BINANCE та продаємо на P2P' not in operation_options_chosen[0]:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = operation_options_chosen || ARRAY['Переводимо на BINANCE та продаємо на P2P']
            WHERE
                (user_id = %s and spread_direction = 8) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 8
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = array_remove(operation_options_chosen, 'Переводимо на BINANCE та продаємо на P2P')
            WHERE
                (user_id = %s and spread_direction = 8) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 8
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings buy-exchange localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_operation_options (user_id,spread_direction,operation_options_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    
    cur.execute("SELECT operation_options_chosen FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 8",(user[0],))
    operation_options_chosen = cur.fetchone()
    
    if 'Переводимо на Bybit и продаємо на P2P' not in operation_options_chosen[0]:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = operation_options_chosen || ARRAY['Переводимо на Bybit и продаємо на P2P']
            WHERE
                (user_id = %s and spread_direction = 8) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 8
                )''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_operation_options SET operation_options_chosen = array_remove(operation_options_chosen, 'Переводимо на Bybit и продаємо на P2P')
            WHERE
                (user_id = %s and spread_direction = 8) AND
                EXISTS (
                    SELECT user_id FROM user_directions_operation_options WHERE user_id = %s and spread_direction = 8
                )''',(user[0],user[0]))
        base.commit()
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings usdt localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'USDT'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['USDT']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'USDT')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings btc localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BTC'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BTC']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BTC')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings eth localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'ETH'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['ETH']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'ETH')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings bnb localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BNB'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BNB']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BNB')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings busd localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'BUSD'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['BUSD']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'BUSD')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings uah localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_cryptocurrency (user_id,spread_direction,cryptocurrency_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT cryptocurrency_chosen FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8",(user[0],))
    cryptocurrency_chosen = cur.fetchone()
    
    if 'UAH'not in cryptocurrency_chosen[0]:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = cryptocurrency_chosen || ARRAY['UAH']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_cryptocurrency SET cryptocurrency_chosen = array_remove(cryptocurrency_chosen, 'UAH')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_cryptocurrency WHERE user_id = %s and spread_direction = 1
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings privatbank localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 8",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'ПриватБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['ПриватБанк']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'ПриватБанк')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings monobank localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 8",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'МоноБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['МоноБанк']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'МоноБанк')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings sportbank localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 8",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'СпортБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['СпортБанк']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'СпортБанк')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")

@settings_directions_router.callback_query(lambda c: c.data ==  'settings rayfazen localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 8",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Райфайзен'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Райфайзен']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Райфайзен')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings pumb localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 8",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Пумб'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Пумб']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Пумб')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings izibank localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 8",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'iziБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['iziБанк']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'iziБанк')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings abank localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 8",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'Абанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['Абанк']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'Абанк')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings obank localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 8",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'ОщадБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['ОщадБанк']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'ОщадБанк')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings otpbank localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 8",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'OTPБанк'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['OTPБанк']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'OTPБанк')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@settings_directions_router.callback_query(lambda c: c.data ==  'settings neobank localbitcoins settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT id FROM users WHERE telegram_id = %s",(str(user_id),))
    user = cur.fetchone()
    
    cur.execute('''INSERT INTO user_directions_banks (user_id,spread_direction,bank_chosen)
        SELECT %s,%s,%s
        WHERE
            NOT EXISTS (
                SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
            )''',(user[0],8,[],user[0]))
    base.commit()
    
    cur.execute("SELECT bank_chosen FROM user_directions_banks WHERE user_id = %s and spread_direction = 8",(user[0],))
    bank_chosen = cur.fetchone()
    
    if 'NEO'not in bank_chosen[0]:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = bank_chosen || ARRAY['NEO']
            WHERE 
            user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    else:
        cur.execute('''UPDATE user_directions_banks SET bank_chosen = array_remove(bank_chosen, 'NEO')
            WHERE 
                user_id = %s and spread_direction = 8 AND
                EXISTS (
                    SELECT user_id FROM user_directions_banks WHERE user_id = %s and spread_direction = 8
                )
            ''',(user[0],user[0]))
        base.commit()
    
    btn = settings_simple_direction(user_id,'localbitcoins settings')
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
    
    
    
    
    
    
    