from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Привет')],
    [KeyboardButton(text='Пока')],
], resize_keyboard=True)

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Новости', url='https://www.rbc.ru/')],
    [InlineKeyboardButton(text='Музыка', url='https://music.yandex.ru/')],
    [InlineKeyboardButton(text='Видео', url='https://www.youtube.com/')]
])

inline_keyboard_dynamic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Показать больше', callback_data='more')],
])

options = ['Опция 1', 'Опция 2']
# options = {'Опция 1': 'Это опция номер 1',
#            'Опция 2': 'Это опция номер 2'}


async def options_kb():
    keyboard = InlineKeyboardBuilder()
    for key in options:
        keyboard.add(InlineKeyboardButton(text=key, callback_data=key))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)
