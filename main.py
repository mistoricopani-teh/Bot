import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from fastapi import FastAPI
import uvicorn

# Настройка логирования (чтобы видеть работу бота в консоли Render)
logging.basicConfig(level=logging.INFO)

# Твой токен и ссылка на WebApp уже вшиты в код для простоты запуска
BOT_TOKEN = "8889129806:AAExgPOn8HN-dMcBPZSA8QxOszCfcySSzy0"
WEBAPP_URL = "https://mistoricopani-teh.github.io/Bot-veb/"

# Инициализация бота и диспетчера aiogram
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем веб-сервер FastAPI. Он нужен, чтобы бесплатный тариф Render не отключал бота.
app = FastAPI()

@app.get("/")
def health_check():
    # Эта страница будет открываться по адресу твоего сервера на Render
    return {"status": "alive", "project": "portfolio-bot"}

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Создаем интерактивную клавиатуру
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            # Кнопка, которая откроет твой сайт прямо внутри Telegram
            InlineKeyboardButton(
                text="🚀 Открыть портфолио",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ],
        [
            # Кнопка быстрой связи (можешь заменить юзернейм на свой)
            InlineKeyboardButton(
                text="✍️ Написать нам",
                url="https://t.me/mistoricopani_teh"  # Сюда вставь свой личный ТГ
            )
        ]
    ])
    
    # Приветственное сообщение
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Добро пожаловать в бот-портфолио наших проектов.\n\n"
        "Нажмите кнопку ниже, чтобы открыть наше интерактивное веб-приложение прямо здесь, внутри Telegram!",
        reply_markup=kb
    )

# Главная функция запуска
async def main():
    # Render автоматически передает порт в переменную окружения PORT. Если её нет, используем 8000.
    port = int(os.getenv("PORT", 8000))
    config = uvicorn.Config(app, host="0.0.0.0", port=port)
    server = uvicorn.Server(config)
    
    # Запускаем параллельно веб-сервер uvicorn и опрос бота Telegram (Long Polling)
    await asyncio.gather(
        server.serve(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
