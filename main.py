import logging
import os
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

import expenses
from categories import Categories
C = Categories()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Welcome message and help"""
    await message.answer(
        "To add expense - 0.8 subway\n"
        "To delete expense - /del 1\n"
        "To see categories - /cat\n"
        "Today analise - /today\n"
        "This month analise - /month\n")


@dp.message_handler(commands=['cat'])
async def categories_list(message: types.Message):
    """Shows the list of available categories"""
    categories = C.get_all_categories()
    answer_message = "Categories:\n\n" +\
        ('\n'.join([c.name+"("+", ".join(c.aliases)+")" for c in categories]))
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Deletes expense"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    await message.answer(
        f"The expense with id {row_id} has been deleted.")


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Shows today statistics of expenses"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Adds expense or answers that message was incorrect"""
    expense = expenses.add_expense(message.text)
    if not expense:
        answer_message = (
            "Invalid format. Please type /help and write correctly.\n\n"
        )
    else:
        answer_message = (
            f"The expense for the amount of {expense.amount} BYN for {expense.category_name} has been added.\n\n"
        )
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
