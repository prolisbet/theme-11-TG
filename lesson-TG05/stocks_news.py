import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
import requests
import logging
from googletrans import Translator

from config import TOKEN, ALPHA_VANTAGE_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

logging.basicConfig(level=logging.INFO)


def translate(text):
    try:
        translated = translator.translate(text, dest='ru', src='en')
        return translated.text
    except Exception as e:
        logging.error(f"Ошибка при получении данных: {e}")
        return "Произошла ошибка при переводе текста."


def get_market_news(number):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        number = int(number)
    except ValueError:
        number = 5
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'feed' in data:
            news_items = data['feed'][:number]  # Количество новостей в запросе
            news_list = []
            for item in news_items:
                title = item.get('title', 'No title')
                summary = item.get('summary', 'No summary')
                url = item.get('url', 'No URL')
                news_list.append(f"{translate(title)}\n{translate(summary)}\nПодробнее: {url}\n")
            stocks_news = "\n\n".join(news_list)
            return stocks_news
        else:
            return "Не удалось получить данные о рынке. Пожалуйста, попробуйте позже."
    except Exception as e:
        logging.error(f"Ошибка при получении данных: {e}")
        return "Произошла ошибка при запросе данных о рынке."


def get_company_overview(symbol):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            name = data.get('Name', 'No Name')
            description = data.get('Description', 'No Description')
            market_cap = data.get('MarketCapitalization', 'No Market Cap')
            pe_ratio = data.get('PERatio', 'No PE Ratio')
            return (f"Компания: {name}\nОписание: {translate(description)}\n"
                    f"Рыночная капитализация: {market_cap}\nP/E Ratio: {pe_ratio}")
        else:
            return "Не удалось получить данные о компании. Пожалуйста, попробуйте позже."
    except Exception as e:
        logging.error(f"Ошибка при получении данных: {e}")
        return "Произошла ошибка при запросе данных о компании."


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот, который может предоставить информацию о рынке ценных бумаг.\n"
                         "Используй команду /market с числом N, чтобы получить N последних новостей.\n"
                         "Используй команду /company с символом акции, чтобы получить данные о компании.\n")


@dp.message(Command('market'))
async def send_market_news(message: Message, command: CommandObject):
    first_message = await message.answer("Запрашиваю данные о рынке...")
    args = command.args
    if not args:
        args = 5  # По умолчанию выдаем 5 последних новостей
    market_news = get_market_news(args)
    await message.answer(market_news)
    await first_message.delete()


@dp.message(Command('company'))
async def send_company_overview(message: Message, command: CommandObject):
    args = command.args
    if not args:
        await message.answer("Пожалуйста, укажите символ компании. Например: /company AAPL")
        return
    first_message = await message.answer(f"Запрашиваю данные о компании {args}...")
    company_overview = get_company_overview(args)
    await message.answer(company_overview)
    await first_message.delete()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
