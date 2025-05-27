import os
import httpx
from aiogram import types
from dotenv import load_dotenv
from backend.gpt import get_gpt_response



load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

async def handle_start(message: types.Message):
    await message.reply(
        "Привет! Пришли мне свои Bybit API ключи в формате:\n<code>API_KEY:API_SECRET</code>"
    )

async def handle_keys(message: types.Message):
    telegram_id = str(message.from_user.id)
    text = message.text.strip()

    if ":" not in text:
        await message.reply("Неверный формат. Пришли ключи так: <code>API_KEY:API_SECRET</code>")
        return

    api_key, api_secret = text.split(":", 1)
    payload = {
        "telegram_id": telegram_id,
        "api_key": api_key,
        "api_secret": api_secret,
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BACKEND_URL}/user/set_keys", params=payload)
            if resp.status_code == 200:
                await message.reply("Ключи успешно сохранены! Теперь можно отправлять торговые команды.")
            else:
                await message.reply("Произошла ошибка при сохранении ключей. Попробуйте позже.")
    except httpx.RequestError as e:
        await message.reply(f"Ошибка при соединении с сервером: {e}")

async def handle_trade_command(message: types.Message):
    telegram_id = str(message.from_user.id)
    user_input = message.text.strip()

    try:
        async with httpx.AsyncClient() as client:
            keys_response = await client.get(f"{BACKEND_URL}/user/get_keys", params={"telegram_id": telegram_id})
            if keys_response.status_code != 200:
                await message.reply("Сначала отправьте свои API-ключи в формате: <code>API_KEY:API_SECRET</code>")
                return
            keys = keys_response.json()

            gpt_response = await client.post(f"{BACKEND_URL}/gpt/parse_command", json={"user_input": user_input})
            if gpt_response.status_code != 200:
                await message.reply("Ошибка при обработке команды через ChatGPT.")
                return

            command_data = gpt_response.json()

            trade_response = await client.post(f"{BACKEND_URL}/bybit/execute", json={
                "api_key": keys["api_key"],
                "api_secret": keys["api_secret"],
                "command": command_data
            })
            if trade_response.status_code != 200:
                await message.reply("Ошибка при выполнении команды на Bybit.")
                return
            result = trade_response.json()
            await message.reply(f"Результат операции: {result}")
    except httpx.RequestError as e:
        await message.reply(f"Ошибка при соединении с сервером: {e}")



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