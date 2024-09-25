import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (Message,
                           ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import random
import requests
import sqlite3
import aiohttp
import logging

from config import TOKEN, EXCHANGE_RATE_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

button_register = KeyboardButton(text='Регистрация в телеграм-боте')
button_exchange_rates = KeyboardButton(text='Курс валют')
button_tips = KeyboardButton(text='Советы по экономии')
button_expenses = KeyboardButton(text='Личные расходы')

kb = ReplyKeyboardMarkup(keyboard=[
    [button_register, button_exchange_rates],
    [button_tips, button_expenses]
], resize_keyboard=True)

conn = sqlite3.connect('user.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category1 TEXT,
    category2 TEXT,
    category3 TEXT,
    expenses1 REAL, 
    expenses2 REAL, 
    expenses3 REAL
    )
''')

conn.commit()


class FinanceForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я ваш личный финансовый помощник. \n'
                         'Выберите одну из опций в меню:', reply_markup=kb)


@dp.message(F.text == 'Регистрация в телеграм-боте')
async def register(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    cur.execute('''
        SELECT * FROM users WHERE telegram_id = ?
    ''', (telegram_id,))
    user = cur.fetchone()
    if user:
        await message.answer('Вы уже зарегистрированы')
    else:
        cur.execute('''
            INSERT INTO users (telegram_id, name) VALUES (?, ?)
        ''', (telegram_id, name,))
        conn.commit()
        await message.answer('Вы успешно зарегистрированы!')


@dp.message(F.text == 'Курс валют')
async def exchange_rates(message: Message):
    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD'
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer('Не удалось получить данные по курсам валют')
            return
        usd_to_rub = data['conversion_rates']['RUB']
        logging.info(usd_to_rub)
        usd_to_euro = data['conversion_rates']['EUR']
        logging.info(usd_to_euro)
        euro_to_rub = usd_to_rub / usd_to_euro
        logging.info(euro_to_rub)

        await message.answer(f"1 USD - {usd_to_rub:.2f} RUB\n"
                             f"1 EUR - {euro_to_rub:.2f} RUB")
    except:
        await message.answer('Произошла ошибка')


@dp.message(F.text == 'Советы по экономии')
async def send_tips(message: Message):
    tips = [
        'Совет №1: \nСоздайте бюджет и строго придерживайтесь его, чтобы контролировать свои расходы.',
        'Совет №2: \nСравнивайте цены перед покупкой, чтобы находить лучшие предложения и скидки.',
        'Совет №3: \nГотовьте пищу дома вместо частого посещения ресторанов и кафе.',
        'Совет №4: \nОткажитесь от ненужных подписок и услуг, которые вы не используете.',
        'Совет №5: \nДелайте покупки оптом на предметы длительного хранения, '
        'чтобы сэкономить в долгосрочной перспективе.'
    ]
    tip = random.choice(tips)
    await message.answer(tip)


@dp.message(F.text == 'Личные расходы')
async def expenses(message: Message, state: FSMContext):
    await state.set_state(FinanceForm.category1)
    await message.reply('Введите первую категорию расходов:')


@dp.message(FinanceForm.category1)
async def expenses(message: Message, state: FSMContext):
    await state.update_data(category1=message.text)
    await state.set_state(FinanceForm.expenses1)
    await message.reply('Введите расходы для первой категории:')


@dp.message(FinanceForm.expenses1)
async def expenses(message: Message, state: FSMContext):
    await state.update_data(expenses1=float(message.text))
    await state.set_state(FinanceForm.category2)
    await message.reply('Введите вторую категорию расходов:')


@dp.message(FinanceForm.category2)
async def expenses(message: Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinanceForm.expenses2)
    await message.reply('Введите расходы для второй категории:')


@dp.message(FinanceForm.expenses2)
async def expenses(message: Message, state: FSMContext):
    await state.update_data(expenses2=float(message.text))
    await state.set_state(FinanceForm.category3)
    await message.reply('Введите третью категорию расходов:')


@dp.message(FinanceForm.category3)
async def expenses(message: Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinanceForm.expenses3)
    await message.reply('Введите расходы для тертьей категории:')


@dp.message(FinanceForm.expenses3)
async def expenses(message: Message, state: FSMContext):
    await state.update_data(expenses3=float(message.text))
    data = await state.get_data()
    telegram_id = message.from_user.id
    cur.execute('''
        UPDATE users SET category1 = ?, category2 = ?, category3 = ?, 
        expenses1 = ?, expenses2 = ?, expenses3 = ? WHERE telegram_id = ?
    ''', (data['category1'], data['category2'], data['category3'],
          data['expenses1'], data['expenses2'], data['expenses3'], telegram_id, ))
    conn.commit()
    await state.clear()
    await message.answer('Категории и расходы сохранены.')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
