import asyncio 
import logging
import sys
import sqlite3

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

import config


dp = Dispatcher()
conn = sqlite3.connect('db_market')


def get_user_by_user_id(user_id: int):
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result


def post_new_user_info(user_id: int):
    cursor = conn.cursor()
    get_user = get_user_by_user_id(user_id)
    if get_user == None:
        cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
    else:
        print('Данный пользователь уже есть в базе данных')


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    post_new_user_info(message.from_user.id)
    await message.answer(f'Привет!!! {html.bold(message.from_user.full_name)}')


async def main():
    bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())