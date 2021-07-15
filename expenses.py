import datetime
import re
from typing import List, NamedTuple, Optional

import pytz

import db
from categories import Categories


class Message(NamedTuple):
    """Class for representing parsed message"""
    amount: int
    category_text: str


class Expense(NamedTuple):
    """Class for representing one expense"""
    id: Optional[int]
    amount: int
    category_name: str


def parse_message(raw_message: str) -> Message:
    """Parses data about new expense"""
    re_result = re.match(r"([\d]+) (.*)", raw_message)
    if not re_result or not re_result.group(0) or not re_result.group(1) or not re_result.group(2):
        return None
        #raise Exception("Invalid format. Please type /help and write correctly.")
    amount = re_result.group(1).replace(" ", "")
    category_text = re_result.group(2).strip().lower()
    return Message(amount=int(amount), category_text=category_text)


def add_expense(raw_message: str) -> Expense:
    """Adds new expense"""
    parsed_message = parse_message(raw_message)
    if not parsed_message:
        return None
    category = Categories().get_category(parsed_message.category_text)
    inserted_row_id = db.insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_datetime(),
        "category_codename": category.codename,
        "raw_text": raw_message
    })
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_name=category.name)


def _get_datetime() -> str:
    """Returns current datetime string formatted"""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")


def delete_expense(row_id: int) -> None:
    """Deletes expense by it's id"""
    db.delete("expense", row_id)


