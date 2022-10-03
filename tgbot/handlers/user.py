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
from tgbot.misc.messages import info

from tgbot.keyboards.inlineBtn import main_page, balance_btn,home_btn,user_settings_btn

import datetime
import asyncio
import json

user_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
cur = base.cursor()

@user_router.message(commands=["start"])
async def user_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    auf = await auf_status(user_id)
    
    if auf:
        cur.execute("SELECT spreads_on from users where telegram_id = %s",(str(user_id),) )
        spreads_on = cur.fetchone()
        btn = main_page(spreads_on[0])
        cur.execute(''' SELECT users.telegram_id,users.spreads_on, users.balance_usdt, us.valid_to, ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                                LEFT JOIN user_subscriptions us on us.user_id = users.id
                        WHERE telegram_id = %s''',(str(user_id),))
        user = cur.fetchone()
        await bot.send_message(user_id,f'''🏠 Главное меню

🎫 Ваш ID: {user_id}
📊 Мин - Макс спред: {user[4] if user[4] else "сперды не настроены"}
{user[3] if user[3] else "🚫 Нет активной подписки"}
💰 Баланс: {user[2]} USDT''',reply_markup=btn.as_markup())
    else:
        await db_update.register_user(user_id,user_name)
        cur.execute(''' SELECT users.telegram_id,users.spreads_on, users.balance_usdt, us.valid_to, ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                                LEFT JOIN user_subscriptions us on us.user_id = users.id
                        WHERE telegram_id = %s''',(str(user_id),))
        user = cur.fetchone()
        cur.execute("SELECT spreads_on from users where telegram_id = %s",(str(user_id),) )
        spreads_on = cur.fetchone()
        btn = main_page(spreads_on[0])
        await bot.send_message(user_id,f'''🏠 Главное меню

🎫 Ваш ID: {user_id}
📊 Мин - Макс спред: {user[4] if user[4] else "сперды не настроены"}
{user[3] if user[3] else "🚫 Нет активной подписки"}
💰 Баланс: {user[2]} USDT''',reply_markup=btn.as_markup())


@user_router.callback_query(lambda c: c.data == 'change spread')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("UPDATE users SET spreads_on = NOT spreads_on WHERE telegram_id = %s", (str(user_id),))
    base.commit()
    cur.execute("SELECT spreads_on from users where telegram_id = %s",(str(user_id),) )
    spreads_on = cur.fetchone()
    btn = main_page(spreads_on[0])
    await callback_query.message.edit_reply_markup(reply_markup=btn.as_markup())
    
    
@user_router.callback_query(lambda c: c.data == 'balance')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT spreads_on from users where telegram_id = %s",(str(user_id),) )
    spreads_on = cur.fetchone()
    btn = balance_btn()
    cur.execute("SELECT balance_usdt from users where telegram_id = %s",(str(user_id),)) 
    balance = cur.fetchone()
    await callback_query.message.edit_text(f'''💰 Баланс: {str(balance[0])} USDT''',reply_markup=btn.as_markup())
    
    
@user_router.callback_query(lambda c: c.data == 'contacts')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = home_btn()
    await callback_query.message.edit_text(info['contacts'],reply_markup=btn.as_markup(),parse_mode="HTML")
    
@user_router.callback_query(lambda c: c.data == 'instructions')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = home_btn()
    await callback_query.message.edit_text(info['instructions'],reply_markup=btn.as_markup(),parse_mode="HTML")
    
    
@user_router.callback_query(lambda c: c.data == 'two hours')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    cur.execute("SELECT trial_version_activated from users where telegram_id = %s",(str(user_id),) )
    trial_version_activated = cur.fetchone()
    if trial_version_activated[0] == False:
        cur.execute("UPDATE users SET trial_version_activated = true WHERE telegram_id = %s", (str(user_id),))
        now = datetime.datetime.now()
        valid_time = now + datetime.timedelta(hours=2)
        # valid_time = now.strftime("%d-%m-%Y %H:%M:%S")
        print(valid_time)
        cur.execute("INSERT INTO user_subscriptions (user_id, valid_to) VALUES (%s, %s)",(user_id,valid_time))
        base.commit()
        
        

    
    
    