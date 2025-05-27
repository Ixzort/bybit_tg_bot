from sqlalchemy import Column, Integer, String
from .database import Base
from pydantic import BaseModel, model_validator
from typing import Optional

class UserKey(Base):
    __tablename__ = "user_keys"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    bybit_api_key = Column(String)
    bybit_api_secret = Column(String)

class OrderRequest(BaseModel):
    symbol: str
    amount: Optional[float] = None
    quote: Optional[float] = None

    @model_validator(mode="after")
    def check_amount_or_quote(self):
        if self.amount is None and self.quote is None:
            raise ValueError('Необходимо указать либо amount, либо quote')
        if self.amount is not None and self.quote is not None:
            raise ValueError('Укажите только одно: amount или quote')
        return self

