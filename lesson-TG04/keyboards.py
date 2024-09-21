from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Тестовая кнопка 1')],
    [KeyboardButton(text='Тестовая кнопка 2'), KeyboardButton(text='Тестовая кнопка 3')],
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Видео', url='https://youtu.be/dQw4w9WgXcQ')],
])

test = ['Кнопка 1', 'Кнопка 2', 'Кнопка 3', 'Кнопка 4']


async def test_kb():
    keyboard = ReplyKeyboardBuilder()
    for key in test:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)


