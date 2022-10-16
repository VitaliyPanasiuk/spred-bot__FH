from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram import Bot, types
from tgbot.config import load_config

from tgbot.misc.functions import auf_status,get_settings_directions
from tgbot.misc.messages import price, spread

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.db import db_update

config = load_config(".env")

base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
cur = base.cursor()

def main_page(spreads_on):
    example = InlineKeyboardBuilder()
    print(spreads_on)
    if spreads_on[1] == False:
        example.row(types.InlineKeyboardButton(
            text='🔥 Використати дві години підписки 🔥',
            callback_data='two hours'
        ))
    example.row(types.InlineKeyboardButton(
        text=f'ℹ️ Спреди  {"увімкнено 🟢" if spreads_on[0] else "вимкнено 🔴"}',
        callback_data='change spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='💰 Баланс',
        callback_data='balance'
    ),types.InlineKeyboardButton(
        text='💥 Підписка',
        callback_data='subscription'
    ))
    example.row(types.InlineKeyboardButton(
        text='⚙️ Налаштування',
        callback_data='settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='📲 Інструкціїї',
        callback_data='instructions'
    ))
    example.row(types.InlineKeyboardButton(
        text='📞 Контакти',
        callback_data='contacts'
    ))
    example.row(types.InlineKeyboardButton(
        text='♻️ Оновити меню',
        callback_data='reload menu'
    ))
    
    return example

def balance_btn():
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text='Поповнити',
        callback_data='donate'
    ))
    example.row(types.InlineKeyboardButton(
        text='Ордера',
        callback_data='orders'
    ))
    example.row(types.InlineKeyboardButton(
        text='Головне меню',
        callback_data='main page'
    ))
    
    return example

def home_btn():
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text='Головне меню',
        callback_data='main page'
    ))
    
    return example

def user_settings_btn():
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text='Обрати напрямки',
        callback_data='choose directions'
    ))
    example.row(types.InlineKeyboardButton(
        text='Налаштувати напрямки',
        callback_data='settings directions'
    ))
    example.row(types.InlineKeyboardButton(
        text='Мінімальний спред',
        callback_data='minimal spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='Головне меню',
        callback_data='main page'
    ))
    
    return example

def choose_directions_btn(arr):
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text=f'Найпростіші (Найліквідніші) зв’язки {"🟢" if arr[0][0] == True else "🔴"}',
        callback_data='simple direction'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'Міжбіржові {"🟢" if arr[1][0] == True else "🔴"}',
        callback_data='interexchange'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'Готівка {"🟢" if arr[2][0] == True else "🔴"}',
        callback_data='cash'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'Binance {"🟢" if arr[3][0] == True else "🔴"}',
        callback_data='binance'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'OKX {"🟢" if arr[4][0] == True else "🔴"}',
        callback_data='okx'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'ByBit {"🟢" if arr[5][0] == True else "🔴"}',
        callback_data='bybit'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'Wise {"🟢" if arr[6][0] == True else "🔴"}',
        callback_data='wise'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'LocalBitcoins {"🟢" if arr[7][0] == True else "🔴"}',
        callback_data='localbitcoins'
    ))
    example.row(types.InlineKeyboardButton(
        text='Повернутися назад',
        callback_data='back to settings'
    ))
    
    return example

def settings_directions_btn():
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text='Найпростіші (Найліквідніші) зв’язки',
        callback_data='simple direction settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='Міжбіржові',
        callback_data='interexchange settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='Готівка',
        callback_data='cash settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='Binance',
        callback_data='binance settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='OKX',
        callback_data='okx settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='ByBit',
        callback_data='bybit settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='Wise',
        callback_data='wise settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='LocalBitcoins',
        callback_data='localbitcoins settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='Повернутися назад',
        callback_data='back to settings'
    ))
    
    return example

def settings_simple_direction(user_id,direction):
    example = InlineKeyboardBuilder()
    if direction == 'simple direction settings':
        settings = get_settings_directions(user_id,'Найпростіші (Найліквідніші) зв’язки')
        example.row(types.InlineKeyboardButton(
            text=f'Binance {"🟢" if settings and settings[0] and "Binance" in settings[0] else "🔴"}',
            callback_data='settings binance ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ByBit {"🟢" if settings and settings[0] and "ByBit" in settings[0] else "🔴"}',
            callback_data='settings bybit ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'OKX {"🟢" if settings and settings[0] and "OKX" in settings[0] else "🔴"}',
            callback_data='settings okx ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ПриватБанк {"🟢" if settings and settings[1] and "ПриватБанк" in settings[1] else "🔴"}',
            callback_data='settings privatbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'МоноБанк {"🟢" if settings and settings[1] and "МоноБанк" in settings[1] else "🔴"}',
            callback_data='settings monobank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'СпортБанк {"🟢" if settings and settings[1] and "СпортБанк" in settings[1] else "🔴"}',
            callback_data='settings sportbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Райфайзен {"🟢" if settings and settings[1] and "Райфайзен" in settings[1] else "🔴"}',
            callback_data='settings rayfazen ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Пумб {"🟢" if settings and settings[1] and "Пумб" in settings[1] else "🔴"}',
            callback_data='settings pumb ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'iziБанк {"🟢" if settings and settings[1] and "iziБанк" in settings[1] else "🔴"}',
            callback_data='settings izibank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Абанк {"🟢" if settings and settings[1] and "Абанк" in settings[1] else "🔴"}',
            callback_data='settings abank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'USDT {"🟢" if settings and settings[2] and "USDT" in settings[2] else "🔴"}',
            callback_data='settings usdt ' +direction
        ))
    elif direction == 'interexchange settings':
        settings = get_settings_directions(user_id,'Міжбіржові')
        example.row(types.InlineKeyboardButton(
            text=f'Binance {"🟢" if settings and settings[0] and "Binance" in settings[0] else "🔴"}',
            callback_data='settings binance ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ByBit {"🟢" if settings and settings[0] and "ByBit" in settings[0] else "🔴"}',
            callback_data='settings bybit ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'OKX {"🟢" if settings and settings[0] and "OKX" in settings[0] else "🔴"}',
            callback_data='settings okx ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ПриватБанк {"🟢" if settings and settings[1] and "ПриватБанк" in settings[1] else "🔴"}',
            callback_data='settings privatbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'МоноБанк {"🟢" if settings and settings[1] and "МоноБанк" in settings[1] else "🔴"}',
            callback_data='settings monobank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'СпортБанк {"🟢" if settings and settings[1] and "СпортБанк" in settings[1] else "🔴"}',
            callback_data='settings sportbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Пумб {"🟢" if settings and settings[1] and "Пумб" in settings[1] else "🔴"}',
            callback_data='settings pumb ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Абанк {"🟢" if settings and settings[1] and "Абанк" in settings[1] else "🔴"}',
            callback_data='settings abank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'USDT {"🟢" if settings and settings[2] and "USDT" in settings[2] else "🔴"}',
            callback_data='settings usdt ' +direction
        ))
    elif direction == 'cash settings':
        settings = get_settings_directions(user_id,'Готівка')
        example.row(types.InlineKeyboardButton(
            text=f'Binance {"🟢" if settings and settings[0] and "Binance" in settings[0] else "🔴"}',
            callback_data='settings binance ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ByBit {"🟢" if settings and settings[0] and "ByBit" in settings[0] else "🔴"}',
            callback_data='settings bybit ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'OKX {"🟢" if settings and settings[0] and "OKX" in settings[0] else "🔴"}',
            callback_data='settings okx ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ПриватБанк {"🟢" if settings and settings[1] and "ПриватБанк" in settings[1] else "🔴"}',
            callback_data='settings privatbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'МоноБанк {"🟢" if settings and settings[1] and "МоноБанк" in settings[1] else "🔴"}',
            callback_data='settings monobank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'СпортБанк {"🟢" if settings and settings[1] and "СпортБанк" in settings[1] else "🔴"}',
            callback_data='settings sportbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Пумб {"🟢" if settings and settings[1] and "Пумб" in settings[1] else "🔴"}',
            callback_data='settings pumb ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Абанк {"🟢" if settings and settings[1] and "Абанк" in settings[1] else "🔴"}',
            callback_data='settings abank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'USDT {"🟢" if settings and settings[2] and "USDT" in settings[2] else "🔴"}',
            callback_data='settings usdt ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BUSD {"🟢" if settings and settings[2] and "BUSD" in settings[2] else "🔴"}',
            callback_data='settings busd ' +direction
        ))
    elif direction == 'binance settings':
        settings = get_settings_directions(user_id,'Binance')
        example.row(types.InlineKeyboardButton(
            text=f'Купуємо крипту, продаємо її {"🟢" if settings and settings[3] and "Купуємо крипту, продаємо її" in settings[3] else "🔴"}',
            callback_data='settings buy-sell crypto ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Купуємо крипту, міняємо на іншу, продаємо як мейкер {"🟢" if settings and settings[3] and "Купуємо крипту, міняємо на іншу, продаємо як мейкер " in settings[3] else "🔴"}',
            callback_data='settings buy-exchange crypto ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ПриватБанк {"🟢" if settings and settings[1] and "ПриватБанк" in settings[1] else "🔴"}',
            callback_data='settings privatbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'МоноБанк {"🟢" if settings and settings[1] and "МоноБанк" in settings[1] else "🔴"}',
            callback_data='settings monobank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'СпортБанк {"🟢" if settings and settings[1] and "СпортБанк" in settings[1] else "🔴"}',
            callback_data='settings sportbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Пумб {"🟢" if settings and settings[1] and "Пумб" in settings[1] else "🔴"}',
            callback_data='settings pumb ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Абанк {"🟢" if settings and settings[1] and "Абанк" in settings[1] else "🔴"}',
            callback_data='settings abank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ОщадБанк {"🟢" if settings and settings[1] and "-" in settings[1] else "🔴"}',
            callback_data='settings obank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'OTPБанк {"🟢" if settings and settings[1] and "OTPБанк" in settings[1] else "🔴"}',
            callback_data='settings otpbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'NEO {"🟢" if settings and settings[1] and "NEO" in settings[1] else "🔴"}',
            callback_data='settings neobank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'USDT {"🟢" if settings and settings[2] and "USDT" in settings[2] else "🔴"}',
            callback_data='settings usdt ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BUSD {"🟢" if settings and settings[2] and "BUSD" in settings[2] else "🔴"}',
            callback_data='settings busd ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BTC {"🟢" if settings and settings[2] and "BTC" in settings[2] else "🔴"}',
            callback_data='settings btc ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BNB {"🟢" if settings and settings[2] and "BNB" in settings[2] else "🔴"}',
            callback_data='settings bnb ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ETH {"🟢" if settings and settings[2] and "ETH" in settings[2] else "🔴"}',
            callback_data='settings eth ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'UAH {"🟢" if settings and settings[2] and "UAH" in settings[2] else "🔴"}',
            callback_data='settings uah ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'SHIB {"🟢" if settings and settings[2] and "SHIB" in settings[2] else "🔴"}',
            callback_data='settings shib ' +direction
        ))
    elif direction == 'okx settings':
        settings = get_settings_directions(user_id,'OKX')
        example.row(types.InlineKeyboardButton(
            text=f'Купуємо крипту, продаємо її {"🟢" if settings and settings[3] and "Купуємо крипту, продаємо її" in settings[3] else "🔴"}',
            callback_data='settings buy-sell crypto ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Купуємо крипту, міняємо на іншу, продаємо як мейкер {"🟢" if settings and settings[3] and "Купуємо крипту, міняємо на іншу, продаємо як мейкер" in settings[3] else "🔴"}',
            callback_data='settings buy-exchange crypto ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ПриватБанк {"🟢" if settings and settings[1] and "ПриватБанк" in settings[1] else "🔴"}',
            callback_data='settings privatbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'МоноБанк {"🟢" if settings and settings[1] and "МоноБанк" in settings[1] else "🔴"}',
            callback_data='settings monobank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'СпортБанк {"🟢" if settings and settings[1] and "СпортБанк" in settings[1] else "🔴"}',
            callback_data='settings sportbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Пумб {"🟢" if settings and settings[1] and "Пумб" in settings[1] else "🔴"}',
            callback_data='settings pumb ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Абанк {"🟢" if settings and settings[1] and "Абанк" in settings[1] else "🔴"}',
            callback_data='settings abank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'USDT {"🟢" if settings and settings[2] and "USDT" in settings[2] else "🔴"}',
            callback_data='settings usdt ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BTC {"🟢" if settings and settings[2] and "BTC" in settings[2] else "🔴"}',
            callback_data='settings btc ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ETH {"🟢" if settings and settings[2] and "ETH" in settings[2] else "🔴"}',
            callback_data='settings eth ' +direction
        ))
    elif direction == 'bybit settings':
        settings = get_settings_directions(user_id,'ByBit')
        example.row(types.InlineKeyboardButton(
            text=f'Купуємо крипту, продаємо її {"🟢" if settings and settings[3] and "Купуємо крипту, продаємо її" in settings[3] else "🔴"}',
            callback_data='settings buy-sell crypto ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Купуємо крипту, міняємо на іншу, продаємо як мейкер {"🟢" if settings and settings[3] and "Купуємо крипту, міняємо на іншу, продаємо як мейкер" in settings[3] else "🔴"}',
            callback_data='settings buy-exchange crypto ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ПриватБанк {"🟢" if settings and settings[1] and "ПриватБанк" in settings[1] else "🔴"}',
            callback_data='settings privatbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'МоноБанк {"🟢" if settings and settings[1] and "МоноБанк" in settings[1] else "🔴"}',
            callback_data='settings monobank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'СпортБанк {"🟢" if settings and settings[1] and "СпортБанк" in settings[1] else "🔴"}',
            callback_data='settings sportbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Пумб {"🟢" if settings and settings[1] and "Пумб" in settings[1] else "🔴"}',
            callback_data='settings pumb ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Абанк {"🟢" if settings and settings[1] and "Абанк" in settings[1] else "🔴"}',
            callback_data='settings abank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'USDT {"🟢" if settings and settings[2] and "USDT" in settings[2] else "🔴"}',
            callback_data='settings usdt ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BTC {"🟢" if settings and settings[2] and "BTC" in settings[2] else "🔴"}',
            callback_data='settings btc ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ETH {"🟢" if settings and settings[2] and "ETH" in settings[2] else "🔴"}',
            callback_data='settings eth ' +direction
        ))
    elif direction == 'wise settings':
        settings = get_settings_directions(user_id,'Wise')
        example.row(types.InlineKeyboardButton(
            text=f'Купуємо крипту та продаємо (одна платіжна система) {"🟢" if settings and settings[3] and "Купуємо крипту та продаємо (одна платіжна система)" in settings[3] else "🔴"}',
            callback_data='settings buy-sell crypto ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Купуємо крипту, конвертуємо на іншу та продаємо (одна платіжна система) {"🟢" if settings and settings[3] and "Купуємо крипту, конвертуємо на іншу та продаємо (одна платіжна система)" in settings[3] else "🔴"}',
            callback_data='settings buy-exchange crypto ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'USDT {"🟢" if settings and settings[2] and "USDT" in settings[2] else "🔴"}',
            callback_data='settings usdt ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BTC {"🟢" if settings and settings[2] and "BTC" in settings[2] else "🔴"}',
            callback_data='settings btc ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ETH {"🟢" if settings and settings[2] and "ETH" in settings[2] else "🔴"}',
            callback_data='settings eth ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BNB {"🟢" if settings and settings[2] and "BNB" in settings[2] else "🔴"}',
            callback_data='settings bnb ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BUSD {"🟢" if settings and settings[2] and "BUSD" in settings[2] else "🔴"}',
            callback_data='settings busd ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'EUR {"🟢" if settings and settings[4] and "EUR" in settings[4] else "🔴"}',
            callback_data='settings eur ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'GBP {"🟢" if settings and settings[4] and "GBP" in settings[4] else "🔴"}',
            callback_data='settings gbp ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'PLN {"🟢" if settings and settings[4] and "PLN" in settings[4] else "🔴"}',
            callback_data='settings pln ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'USD {"🟢" if settings and settings[4] and "USD" in settings[4] else "🔴"}',
            callback_data='settings usd ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'UAH {"🟢" if settings and settings[4] and "UAH" in settings[4] else "🔴"}',
            callback_data='settings uah ' +direction
        ))
    elif direction == 'localbitcoins settings':
        settings = get_settings_directions(user_id,'LocalBitcoins')
        example.row(types.InlineKeyboardButton(
            text=f'Переводимо на BINANCE та продаємо на P2P {"🟢" if settings and settings[3] and "Переводимо на BINANCE та продаємо на P2P" in settings[3] else "🔴"}',
            callback_data='settings buy-sell crypto ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Переводимо на Bybit и продаємо на P2P {"🟢" if settings and settings[3] and "Переводимо на Bybit и продаємо на P2P" in settings[3] else "🔴"}',
            callback_data='settings buy-exchange crypto ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ПриватБанк {"🟢" if settings and settings[1] and "ПриватБанк" in settings[1] else "🔴"}',
            callback_data='settings privatbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'МоноБанк {"🟢" if settings and settings[1] and "МоноБанк" in settings[1] else "🔴"}',
            callback_data='settings monobank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'СпортБанк {"🟢" if settings and settings[1] and "СпортБанк" in settings[1] else "🔴"}',
            callback_data='settings sportbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Пумб {"🟢" if settings and settings[1] and "Пумб" in settings[1] else "🔴"}',
            callback_data='settings pumb ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'Абанк {"🟢" if settings and settings[1] and "Абанк" in settings[1] else "🔴"}',
            callback_data='settings abank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ОщадБанк {"🟢" if settings and settings[1] and "ОщадБанк" in settings[1] else "🔴"}',
            callback_data='settings obank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'OTPБанк {"🟢" if settings and settings[1] and "OTPБанк" in settings[1] else "🔴"}',
            callback_data='settings otpbank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'NEO {"🟢" if settings and settings[1] and "NEO" in settings[1] else "🔴"}',
            callback_data='settings neobank ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'USDT {"🟢" if settings and settings[2] and "USDT" in settings[2] else "🔴"}',
            callback_data='settings usdt ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BTC {"🟢" if settings and settings[2] and "BTC" in settings[2] else "🔴"}',
            callback_data='settings btc ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'ETH {"🟢" if settings and settings[2] and "ETH" in settings[2] else "🔴"}',
            callback_data='settings eth ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BNB {"🟢" if settings and settings[2] and "BNB" in settings[2] else "🔴"}',
            callback_data='settings bnb ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'BUSD {"🟢" if settings and settings[2] and "BUSD" in settings[2] else "🔴"}',
            callback_data='settings busd ' +direction
        ))
        example.row(types.InlineKeyboardButton(
            text=f'UAH {"🟢" if settings and settings[2] and "UAH" in settings[2] else "🔴"}',
            callback_data='settings uah ' +direction
        ))
    
    example.row(types.InlineKeyboardButton(
        text='Повернутися назад',
        callback_data='back to settings direction'
    ))
    example.row(types.InlineKeyboardButton(
        text='Головне меню',
        callback_data='main page'
    ))
    return example

def min_spread_settings_btn():
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text='Найпростіші (Найліквідніші) зв’язки',
        callback_data='simple direction spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='Міжбіржові',
        callback_data='interexchange spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='Готівка',
        callback_data='cash spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='Binance',
        callback_data='binance spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='OKX',
        callback_data='okx spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='ByBit',
        callback_data='bybit spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='Wise',
        callback_data='wise spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='LocalBitcoins',
        callback_data='localbitcoins spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='Повернутися назад',
        callback_data='back to settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='Головне меню',
        callback_data='main page'
    ))
    
    return example

def sub_btn():
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text=f'Активувати промокод',
        callback_data='activate promo'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'1 година = {price["1 hour"]} USDT',
        callback_data='buy 1 hour'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'1 день = {price["1 day"]} USDT',
        callback_data='buy 1 day'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'7 днів = {price["7 day"]} USDT',
        callback_data='buy 7 day'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'1 місяць = {price["1 month"]} USDT',
        callback_data='buy 1 month'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'3 місяці = {price["3 month"]} USDT',
        callback_data='buy 3 month'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'1 рік = {price["1 year"]} USDT',
        callback_data='buy 1 year'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'Назавжди = {price["forever"]} USDT',
        callback_data='buy forever'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'Головне меню',
        callback_data='main page'
    ))
    
    return example




