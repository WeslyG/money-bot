from typing import Literal, Union
from datetime import datetime

from src.type.type import bank_list_type, my_type, transaction_type

class Transaction:
    # PayDict
    # transaction: PayDict = {}

    def __init__(self,
                author: str,
                bank: bank_list_type,
                payed: float | None = None,
                price: float | None = None,
                cashback: float = 0,
                category: str | None = None,
                shop: str | None = None,
                for_who: str = my_type,
                description: str = '',
                type: transaction_type = 'Расход',
                constant: bool = False,
                ):
        # TODO: Тут возможны проблемы с датой при записи в бд
        self.data = datetime.today().strftime("%Y-%m-%d")
        self.author = author

        # me own raw
        self.for_who = for_who
        # str
        self.description = description
        # enum
        self.type = type
        # bool
        self.constant = constant
        # TODO: тянуть лист из эластика
        self.shop = shop
        # TODO: тянуть лист из эластика
        self.category = category
        # TODO: тянуть лист из эластика
        self.bank = bank
        # int
        self.cashback = cashback
        # int
        self.price = price
        # int
        self.payed = payed

    def pretty_print(self) -> str:
        return (
            f'{self.author} {self.type.capitalize()} от {self.data}\n'
            f'Банк - {self.bank}\n'
            f'Кому - {self.for_who}\n'
            f'Постоянная - {self.constant}\n'
            f'Категория - {self.category or "(обязательно)"}\n'
            f'Магазин - {self.shop or "(обязательно)"}\n'
            f'Описание - {self.description or "не задано"} {"" if self.description else "(необязательно)"}\n'
            f'------------------------\n'
            f'Заплачено - {self.payed or "(обязательно)"}\n'
            f'Цена - {self.price or "не задано"} {"" if self.price else "(необязательно)"}\n'
            f'Кэшбек - {self.cashback } {"" if self.cashback else "(необязательно)"}'
        )

    def set_cashback(self, cashback: float):
        self.cashback = cashback

    def set_price(self, price: float):
        self.price = price

    def set_payed(self, payed: float):
        if self.price == None and self.cashback == 0:
            self.payed = payed
            self.price = payed
        else:
            self.payed = payed

    def change_constant(self):
        self.constant = not self.constant

    def change_description(self, description: str):
        self.description = description

    def change_who(self, for_who: str ):
        self.for_who = for_who

    def change_type(self, type: transaction_type):
        self.type = type

    def change_category(self, category_name: str):
        # list!!
        self.category = category_name

    def change_shop(self, shop_name: str):
        # maybe list?
        self.shop = shop_name

    def change_bank(self, bank_name: bank_list_type):
        self.bank = bank_name

    def save(self):
        # validate tree field
        # payed required
        # cachback !> price

        
        # write to db
        pass