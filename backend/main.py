from fastapi import FastAPI, HTTPException, Depends
from .models import OrderRequest
from . import bybit_client
import logging
from . import crud
from . import database
from .database import get_db
from sqlalchemy.ext.asyncio import AsyncSession



# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Bybit GPT Testnet API")

@app.get("/user/get_keys")
async def get_keys(telegram_id: str, db: AsyncSession = Depends(get_db)):
    user_key = await crud.get_user_key(db, telegram_id)
    if not user_key:
        raise HTTPException(status_code=404, detail="Ключи не найдены")
    return {
        "api_key": user_key.bybit_api_key,
        "api_secret": user_key.bybit_api_secret
    }

@app.post("/user/set_keys")
async def set_keys(telegram_id: str, api_key: str, api_secret: str, db: AsyncSession = Depends(get_db)):
    await crud.set_user_key(db, telegram_id, api_key, api_secret)
    return {"message": "Ключи успешно сохранены"}

@app.get("/portfolio")
def get_portfolio():
    try:
        balance = bybit_client.get_balance()
        return balance
    except Exception as e:
        logger.error(f"Ошибка при получении баланса: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении баланса")

@app.post("/buy")
def buy_crypto(request: OrderRequest):
    try:
        market_unit = "baseCoin" if request.amount else "quoteCoin"
        amount = request.amount if request.amount else request.quote
        order = bybit_client.place_market_order(request.symbol, amount, market_unit)
        return order
    except Exception as e:
        logger.error(f"Ошибка при выполнении покупки: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при выполнении покупки")

@app.get("/pnl")
def get_pnl(symbol: str):
    try:
        pnl_data = bybit_client.get_pnl(symbol)
        return pnl_data
    except Exception as e:
        logger.error(f"Ошибка при получении PnL: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении PnL")
