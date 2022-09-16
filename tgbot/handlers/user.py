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

from tgbot.keyboards.inlineBtn import main_page

import datetime
import asyncio
import json

user_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(config.db.db_uri, sslmode="require")
cur = base.cursor()

@user_router.message(commands=["start"])
async def user_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    auf = await auf_status(user_id)
    btn = main_page()
    if auf:
        cur.execute(''' SELECT users.telegram_id,users.spreads_on, users.balance_usdt, us.valid_to, ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                                LEFT JOIN user_subscriptions us on us.user_id = users.id
                        WHERE telegram_id = %s''',(str(user_id),))
        user = cur.fetchone()
        await bot.send_message(user_id,f'''
🏠 Главное меню

🎫 Ваш ID: {user_id}
📊 Мин - Макс спред: {user[4] if user[4] else "сперды не настроены"}
{user[3] if user[3] else "🚫 Нет активной подписки"}
💰 Баланс: {user[2]} USDT                           
        ''',reply_markup=btn.as_markup())
    else:
        await db_update.register_user(user_id,user_name)
        cur.execute(''' SELECT users.telegram_id,users.spreads_on, users.balance_usdt, us.valid_to, ms.spread_value
                            FROM users
                                LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                                LEFT JOIN user_subscriptions us on us.user_id = users.id
                        WHERE telegram_id = %s''',(str(user_id),))
        user = cur.fetchone()
        await bot.send_message(user_id,'''
🏠 Главное меню

🎫 Ваш ID: {user_id}
📊 Мин - Макс спред: {user[4] if user[4] else "сперды не настроены"}
{user[3] if user[3] else "🚫 Нет активной подписки"}
💰 Баланс: {user[2]} USDT                          
        ''',reply_markup=btn.as_markup())
