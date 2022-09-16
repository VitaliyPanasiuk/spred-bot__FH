from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram import Bot, types


def main_page():
    example = InlineKeyboardBuilder()
    example.row(types.InlineKeyboardButton(
        text='Использовать два часа подписки',
        callback_data='confirm'
    ))
    example.row(types.InlineKeyboardButton(
        text='Загрузить спреды',
        callback_data='skip'
    ))
    example.row(types.InlineKeyboardButton(
        text='Спреды включены',
        callback_data='skip'
    ))
    example.row(types.InlineKeyboardButton(
        text='Баланс',
        callback_data='skip'
    ),types.InlineKeyboardButton(
        text='Подписка',
        callback_data='skip'
    ))
    example.row(types.InlineKeyboardButton(
        text='Настройки',
        callback_data='skip'
    ))
    example.row(types.InlineKeyboardButton(
        text='Инструкции',
        callback_data='skip'
    ))
    example.row(types.InlineKeyboardButton(
        text='Контакты',
        callback_data='skip'
    ))
    example.row(types.InlineKeyboardButton(
        text='Обновить меню',
        callback_data='skip'
    ))
    
    return example
