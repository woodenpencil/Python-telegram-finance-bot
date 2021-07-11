import logging
import os
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

import expenses
from categories import Categories
from db import erase_all_tables

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Welcome message and help"""
    await message.answer(
        "This is the financial bot")


@dp.message_handler(lambda message: message.text.startswith('del'))
async def del_expense(message: types.Message):
    """Deletes expense"""
    pass


@dp.message_handler()
async def add_expense(message: types.Message):
    """Adds expense"""
    expense = expenses.add_expense(message.text)
    answer_message = (
        f"The expense for the amount of {expense.amount} BYN for {expense.category_name} has been added.\n\n"

    )
    await message.answer(answer_message)


if __name__ == '__main__':
    #erase_all_tables()     
    executor.start_polling(dp, skip_updates=True)


