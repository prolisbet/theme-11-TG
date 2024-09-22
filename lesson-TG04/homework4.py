import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from config import TOKEN
import random
import requests

import keyboards_hw as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я твой бот на каждый день!', reply_markup=kb.main)


@dp.message(F.text == 'Привет')
async def hello(message: Message):
    try:
        name = message.from_user.full_name
    except:
        name = 'человек! Задай username телеграма'
    await message.answer(f'Привет, {name}!')


@dp.message(F.text == 'Пока')
async def hello(message: Message):
    try:
        name = message.from_user.full_name
    except:
        name = 'человек! Задай username телеграма'
    await message.answer(f'Пока, {name}!')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Этот бот умеет выполнять команды: \n /start \n /help \n /links \n /dynamic'
    )


@dp.message(Command('links'))
async def links(message: Message):
    await message.answer('Вот ссылки на контент:', reply_markup=kb.inline_keyboard)


@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer('Есть несколько опций...', reply_markup=kb.inline_keyboard_dynamic)


@dp.callback_query(F.data == 'more')
async def more(callback: CallbackQuery):
    await callback.answer('Опции подгружаются...')
    await callback.message.edit_text('Есть две опции:', reply_markup=await kb.options_kb())


@dp.callback_query(F.data == 'Опция 1')
async def option1(callback: CallbackQuery):
    await callback.answer('Опция подгружается...')
    await callback.message.answer('Это текст опции номер 1')


@dp.callback_query(F.data == 'Опция 2')
async def option1(callback: CallbackQuery):
    await callback.answer('Опция подгружается...')
    await callback.message.answer('Это текст опции номер 2')


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
