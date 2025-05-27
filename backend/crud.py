from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import UserKey

async def get_user_key(db: AsyncSession, telegram_id: str):
    result = await db.execute(select(UserKey).where(UserKey.telegram_id == telegram_id))
    return result.scalars().first()

async def set_user_key(db: AsyncSession, telegram_id: str, api_key: str, api_secret: str):
    user_key = await get_user_key(db, telegram_id)
    if user_key:
        user_key.bybit_api_key = api_key
        user_key.bybit_api_secret = api_secret
    else:
        user_key = UserKey(
            telegram_id=telegram_id,
            bybit_api_key=api_key,
            bybit_api_secret=api_secret
        )
        db.add(user_key)
    await db.commit()
    return user_key
