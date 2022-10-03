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

from tgbot.keyboards.inlineBtn import main_page, balance_btn,home_btn,user_settings_btn,choose_directions_btn,settings_directions_btn

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
    btn = choose_directions_btn()
    await callback_query.message.edit_text('Выберите направление',reply_markup=btn.as_markup(),parse_mode="HTML")
    
@user_settings_router.callback_query(lambda c: c.data == 'settings directions')
async def user_start(callback_query: types.CallbackQuery, state = FSMContext):
    user_id = callback_query.from_user.id
    btn = settings_directions_btn()
    await callback_query.message.edit_text('Налаштувати напрямок',reply_markup=btn.as_markup(),parse_mode="HTML")