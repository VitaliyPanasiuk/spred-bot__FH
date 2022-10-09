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

from tgbot.keyboards.inlineBtn import main_page,user_settings_btn,settings_directions_btn

import datetime
import asyncio
import json

system_callback_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
cur = base.cursor()


@system_callback_router.callback_query(lambda c: c.data == 'main page')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT spreads_on from users where telegram_id = %s",(str(user_id),) )
    spreads_on = cur.fetchone()
    btn = main_page(spreads_on[0])
    cur.execute(''' SELECT users.telegram_id,users.spreads_on, users.balance_usdt, us.valid_to, ms.spread_value
                            FROM users
                                LEFT JOIN is_direction_on_for_user isd on isd.user_id = users.id and isd.is_on = true
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id and ms.spread_direction = isd.spread_direction
                                LEFT JOIN user_subscriptions us on us.user_id = users.id
                        WHERE telegram_id = %s''',(str(user_id),))
    user = cur.fetchone()
    await callback_query.message.edit_text(f'''🏠 Головне меню

🎫 Ваш ID: {user_id}
📊 Мін - Макс спред: {user[4] if user[4] else "спреди не налаштовані"}
{user[3].strftime("%m/%d/%Y, %H:%M") if user[3] else "🚫 Відсутня активна підписка"}
💰 Баланс: {user[2]} USDT''',reply_markup=btn.as_markup())
    
@system_callback_router.callback_query(lambda c: c.data == 'reload menu')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT spreads_on from users where telegram_id = %s",(str(user_id),) )
    spreads_on = cur.fetchone()
    btn = main_page(spreads_on[0])
    cur.execute(''' SELECT users.telegram_id,users.spreads_on, users.balance_usdt, us.valid_to, ms.spread_value
                            FROM users
                                LEFT JOIN is_direction_on_for_user isd on isd.user_id = users.id and isd.is_on = true
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id and ms.spread_direction = isd.spread_direction
                                LEFT JOIN user_subscriptions us on us.user_id = users.id
                        WHERE telegram_id = %s''',(str(user_id),))
    user = cur.fetchone()
    text = f'''🏠 Головне меню

🎫 Ваш ID: {user_id}
📊 Мін - Макс спред: {user[4] if user[4] else "спреди не налаштовані"}
{user[3].strftime("%m/%d/%Y, %H:%M") if user[3] else "🚫 Відсутня активна підписка"}
💰 Баланс: {user[2]} USDT'''
    if text != str(callback_query.message.text):
        await callback_query.message.edit_text(text,reply_markup=btn.as_markup())

@system_callback_router.callback_query(lambda c: c.data == 'back to settings')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = user_settings_btn()
    await callback_query.message.edit_text('Налаштування',reply_markup=btn.as_markup(),parse_mode="HTML")
        
@system_callback_router.callback_query(lambda c: c.data == 'back to settings direction')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_directions_btn()
    await callback_query.message.edit_text('Налаштувати напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")
        
        
        
        
        
        
        
        
        
        
        