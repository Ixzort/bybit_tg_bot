import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from backend.gpt import get_gpt_response

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def handle_start(message: types.Message):
    await message.reply("Привет! Я бот, интегрированный с ChatGPT. Задайте мне вопрос.")

@dp.message()
async def handle_message(message: types.Message):
    user_input = message.text.strip()
    if not user_input:
        await message.reply("Пожалуйста, введите сообщение.")
        return

    try:
        response = await get_gpt_response(user_input)
        await message.reply(response)
    except Exception as e:
        await message.reply("Произошла ошибка при обработке запроса.")
        print(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
