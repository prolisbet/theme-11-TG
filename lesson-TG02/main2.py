import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, API_WEATHER_KEY
import random
import requests
from gtts import gTTS
import os
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}! Я твой бот на каждый день!')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Этот бот умеет выполнять команды: \n /start \n /help \n /today \n /weather \n /video \n /audio'
    )


@dp.message(F.text.lower() == 'что такое ии?' or F.text.lower() == 'что такое ии')
async def aitext(message: Message):
    await message.answer('Искусственный интеллект - это область '
                         'компьютерных наук, занимающаяся созданием систем, '
                         'способных выполнять задачи, которые требуют человеческого '
                         'интеллекта, такие как обучение, распознавание речи, '
                         'принятие решений и решение проблем.')


@dp.message(F.photo)
async def react_to_photo(message: Message):
    list = ['Классная фотка!', 'Не понял, это что?', 'Не отправляй мне такое больше']
    await message.answer(random.choice(list))
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')


@dp.message(Command('today', prefix='!'))
async def today(message: Message):
    photos = ['https://amicus-vet.ru/images/statii/a582d6cs-960.jpg',
              'https://barboss-etalon.ru/thumb/2/2widh2NIj7_je4A7aeZhNg/580r450/d/Fun__anim__4.jpg',
              'https://cdnn21.img.ria.ru/images/152393/00/1523930015_0:0:2048:2048_1920x0_80_0_0_53a68dd25d62e2fdbb245e12db24e5b6.jpg',
              'https://dezstancya.ru/wp-content/uploads/2018/10/15_1.jpg']
    await message.answer_photo(photo=random.choice(photos), caption='Кто ты сегодня')


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('programmer-designer_video.mp4')
    await bot.send_video(message.chat.id, video)


@dp.message(Command('audio'))
async def audio(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    audio = FSInputFile('Cinematic-Orchestra-Opener_audio.m4a')
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('doc'))
async def doc(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_document')
    doc = FSInputFile('Синтаксис в Python.pdf')
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1: \n 1. Скручивания: 3 подхода по 15 повторений \n 2. Велосипед: 3 подхода по 20 повторений (каждая сторона) \n 3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2: \n 1. Подъемы ног: 3 подхода по 15 повторений \n 2. Русский твист: 3 подхода по 20 повторений (каждая сторона) \n 3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3: \n 1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений \n 2. Горизонтальные ножницы: 3 подхода по 20 повторений \n 3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    random_training = random.choice(training_list)
    await message.answer(f'Это ваша мини-тренировка на сегодня:\n{random_training}')
    tts = gTTS(text=random_training, lang='ru')
    tts.save('training.ogg')
    audio = FSInputFile('training.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove('training.ogg')


@dp.message(Command('weather'))
async def weather(message: Message):
    city = 'Moscow'
    weather_data = get_weather(city)

    description = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']

    weather_info = (
        f"Погода в Москве:\n"
        f"Описание: {description.capitalize()}\n"
        f"Температура: {temp}°C\n"
        f"Ощущается как: {feels_like}°C\n"
        f"Влажность: {humidity}%\n"
        f"Скорость ветра: {wind_speed} м/с"
    )

    await message.answer(weather_info)


def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER_KEY}&units=metric&lang=ru'
    response = requests.get(url)
    return response.json()


@dp.message(F.text)
async def translate(message: Message):
    try:
        translated = translator.translate(message.text, dest='en', src='ru')
        await message.answer(translated.text)
    except Exception as e:
        await message.answer("Произошла ошибка при переводе текста.")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
