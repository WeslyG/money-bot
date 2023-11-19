from datetime import datetime
from typing import Literal, TypedDict

bank_list_type = Literal['Альфа', 'Яндекс', 'Озон', 'Тинек', 'Сбер']

class User(TypedDict):
    name: str
    bank: bank_list_type
    chat_id: str

class PayDict(TypedDict):
    Автор: str
    Дата: str
    Банк: bank_list_type
    Магазин: str
    Описание: str
    Категория: str
    Постоянная: bool
    Кому: str
    Цена: float
    Заплачено: float
    Кэшбек: float
    Тип: str

transaction_type = Literal['Доход','Расход']
my_type = 'себе'
own_type = 'семья'