import asyncio
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

load_dotenv()

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет!\n'
                         f'Это твой крипто-бот, с помощью него ты сможешь:\n'
                         f' - Открывать/Закрывать сделки \U0001F4C8 \n'
                         f' - Проверять текущий баланс \U0001F4B5 \n'
                         f' - Получение статуса каждой сделки по её id \U0001F4CB \n'
                         f' - Получение информации о текущих и завершенных сделках \U0001F4CA \n')


@dp.message(Command('check_balance'))
async def check_balance(message: Message):
    await message.answer("Успешно! Проверка баланса...")


@dp.message(Command('cancel_odred'))
async def cancel_order(message: Message):
    order_id = message.get_args()
    await message.answer(f"Успешно! Отмена заказа с ID: {order_id}...")


@dp.message(Command('order_status'))
async def order_status(message: Message):
    order_id = message.get_args()
    await message.answer(f"Успешно! Статус заказа с ID: {order_id}...")


@dp.message(Command('trading_info'))
async def trading_info(message: Message):
    await message.answer("Успешно! Получение информации о торговле...")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Code's Exited")
