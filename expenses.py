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
    db.insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_datetime_formatted(),
        "category_codename": category.codename,
        "raw_text": raw_message
    })
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_name=category.name)


def _get_datetime_formatted() -> str:
    """Returns current datetime string formatted"""
    return _get_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_datetime() -> datetime.datetime:
    """Returns current datetime"""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def delete_expense(row_id: int) -> None:
    """Deletes expense by it's id"""
    db.delete("expense", row_id)


def get_today_statistics() -> str:
    """Returns statistics of expenses for today"""
    all_today_expenses = db.get_today_expenses()
    base_today_expenses = db.get_today_base_expenses()
    return (f"Expenses for today:\n"
            f"Total - {all_today_expenses} BYN\n\n"
            f"Base - {base_today_expenses} BYN of {_get_budget_limit()} BYN\n\n")


def get_month_statistics() -> str:
    """Returns statistics of expenses for this month"""
    now = _get_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    all_month_expenses = db.get_month_expenses(first_day_of_month)
    base_month_expenses = db.get_month_base_expenses(first_day_of_month)
    now = datetime.date.today().day
    return (f"Expenses for this month:\n"
            f"Total - {all_month_expenses}\n"
            f"Base - {base_month_expenses} BYN of {now * _get_budget_limit()}")


def _get_budget_limit() -> int:
    """Returns day limit for base expenses"""
    return db.fetch_all("budget", ["daily_limit"])[0]["daily_limit"]