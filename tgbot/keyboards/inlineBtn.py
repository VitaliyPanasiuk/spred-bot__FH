from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram import Bot, types


def main_page(spreads_on):
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text='🔥 Использовать два часа подписки 🔥',
        callback_data='two hours'
    ))
    example.row(types.InlineKeyboardButton(
        text='📊 Загрузить спреды',
        callback_data='download spread'
    ))
    example.row(types.InlineKeyboardButton(
        text=f'ℹ️ Спреды включены {"🟢" if spreads_on else "🔴"}',
        callback_data='change spread'
    ))
    example.row(types.InlineKeyboardButton(
        text='💰 Баланс',
        callback_data='balance'
    ),types.InlineKeyboardButton(
        text='💥 Подписка',
        callback_data='subscription'
    ))
    example.row(types.InlineKeyboardButton(
        text='⚙️ Настройки',
        callback_data='settings'
    ))
    example.row(types.InlineKeyboardButton(
        text='📲 Инструкции',
        callback_data='instructions'
    ))
    example.row(types.InlineKeyboardButton(
        text='📞 Контакты',
        callback_data='contacts'
    ))
    example.row(types.InlineKeyboardButton(
        text='♻️ Обновить меню',
        callback_data='reload menu'
    ))
    
    return example

def balance_btn():
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text='Пополнить',
        callback_data='donate'
    ))
    example.row(types.InlineKeyboardButton(
        text='Ордера',
        callback_data='orders'
    ))
    example.row(types.InlineKeyboardButton(
        text='Главное меню',
        callback_data='main page'
    ))
    
    return example

def home_btn():
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text='Главное меню',
        callback_data='main page'
    ))
    
    return example
