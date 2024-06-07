import asyncio
from aiogram import Bot, Dispatcher
import os
from core.utils.statesform import StepsForm, TypeSteps
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import logging
from place_order import check_balance


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
                         f' - Проверять текущий баланс \U0001F4B3 \n'
                         f' - Получать статус каждой сделки по её id \U0001F4CB \n'
                         f' - Получать информациию о текущих и завершенных сделках\U0001F4CA')


@dp.message(Command('cancel_order'))
async def cancel_order(message: Message, state: FSMContext):
    await message.answer(f"Ожидаю id")
    await state.set_state(StepsForm.GET_ID)


@dp.message(StepsForm.GET_ID)
async def get_id(message: Message, state: FSMContext):
    await message.answer('Получил id заказа, выполняю... \U0001F680')
    ido = message.text
    await state.update_data(ido=ido)
    await state.clear()
    await message.answer('Успех!')


@dp.message(Command('check_balance'))
async def check_wallet(message: Message, state: FSMContext):
    await message.answer("Введите тип аккаунта!")
    await state.set_state(TypeSteps.GET_TYPE)


@dp.message(TypeSteps.GET_TYPE)
async def get_type(message: Message, state: FSMContext):
    await message.answer('Получил тип аккаунта, выполняю... \U0001F680')
    account = message.text
    if account == 'UNIFIED' or 'CONTRACT' or 'SPOT':
        totalwalletbalance, coin_type, availablebalance = check_balance(account)
        await state.update_data(account=account)
        await state.clear()
        await message.answer(f'Ваш баланс: {totalwalletbalance} | {coin_type} \U0001F4B3\n'
                             f'Доступные средства: {availablebalance} \U0001F4B8')
    else:
        await message.answer('Введите один из типов аккаунта: UNIFIED, CONTRACT, SPOT!')


@dp.message(Command('order_status'))
async def order_status(message: Message):
    order_id = message.get_args()
    if not order_id:
        await message.answer("Пожалуйста, укажите ID заказа после команды. Например: /order_status 123")
        return
    await message.answer(f"Успешно! Статус заказа с ID: {order_id}...")


@dp.message(Command('trading_info'))
async def trading_info(message: Message):
    await message.answer("Успешно! Получение информации о торговле...")


async def main():
    await dp.start_polling(bot)
    dp.message.register(get_id, StepsForm.GET_ID)
    dp.message.register(get_type, TypeSteps.GET_TYPE)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Code's Exited")
