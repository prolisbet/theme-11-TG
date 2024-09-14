import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, API_WEATHER_KEY
import random
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я твой бот на каждый день!')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Этот бот умеет выполнять команды: \n /start \n /help \n /today \n /weather'
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


@dp.message(Command('today'))
async def today(message: Message):
    photos = ['https://amicus-vet.ru/images/statii/a582d6cs-960.jpg',
              'https://barboss-etalon.ru/thumb/2/2widh2NIj7_je4A7aeZhNg/580r450/d/Fun__anim__4.jpg',
              'https://cdnn21.img.ria.ru/images/152393/00/1523930015_0:0:2048:2048_1920x0_80_0_0_53a68dd25d62e2fdbb245e12db24e5b6.jpg',
              'https://dezstancya.ru/wp-content/uploads/2018/10/15_1.jpg']
    await message.answer_photo(photo=random.choice(photos), caption='Кто ты сегодня')


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
