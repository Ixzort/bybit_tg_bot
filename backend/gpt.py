import os
import json
from dotenv import load_dotenv
import openai

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Переменная окружения OPENAI_API_KEY не установлена.")

openai.api_key = api_key

async def parse_command_with_gpt(user_input: str) -> dict:
    system_prompt = (
        "Ты помощник по криптоторговле. Отвечай только в формате JSON: "
        '{"action": "buy", "symbol": "BTCUSDT", "amount": 0.001}'
    )
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ]
        )
        raw = response.choices[0].message.content.strip()

        # Удаление возможных маркеров форматирования
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Не удалось распарсить JSON-ответ: {raw}") from e
    except Exception as e:
        raise RuntimeError(f"Ошибка при обращении к OpenAI API: {str(e)}") from e

async def get_gpt_response(user_input: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Ошибка при обращении к OpenAI API: {str(e)}") from e