from dataclasses import dataclass
from datetime import datetime


@dataclass
class News:
    id: int
    title: str
    link: str
    date: datetime

    def __str__(self):
        return f'{self.id}.\t{self.title}\n\t{"-" * len(self.title)}\n\t{self.link}\n' \
               f'\tDate: {self.date}\n'


@dataclass
class Company:
    name: str
    symbol: str
    url: str


@dataclass
class Promotion:
    company: Company
    buy_to: str
    register: str
    price: str
    lot: str
    dividend: str
    income: str
