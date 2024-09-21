import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, API_WEATHER_KEY
import random
import requests

import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я твой бот на каждый день!', reply_markup=await kb.test_kb())


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Этот бот умеет выполнять команды: \n /start \n /help \n'
    )


@dp.message()
async def echo(message: Message):
    if message.text.lower() == 'тест':
        await message.answer('Тестируем...')
    else:
        await message.send_copy(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
