import asyncio
import sqlite3
import time
from aiogram import Bot, Dispatcher
import os
from core.utils.statesform import StepsForm
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from place_order import check_balance, get_orders, cancel_order
from signals_parse import get_signal

load_dotenv()

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher()

conn = sqlite3.connect('accounts.db')

cur = conn.cursor()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет!\n'
                         f'Это твой крипто-бот, с помощью него ты сможешь:\n'
                         f' - Открывать/Закрывать сделки \U0001F4C8 \n'
                         f' - Проверять текущий баланс \U0001F4B3 \n'
                         f' - Получать статус каждой сделки по её id \U0001F194 \n'
                         f' - Получать информациию о текущих и завершенных сделках\U0001F4CA')


@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer('Привет, это крипто-бот \U0001F44B\n'
                         '\n'
                         'Все необходимые инструкции будут при вызове команд \U0001F4EB\n'
                         '\n'
                         "Чтобы получить список команд, нажми на нижнюю левую кнопку 'menu' \U00002199\n"
                         "\n"
                         'Удачного трейдинга \U0001F340')


@dp.message(Command('cancel_order'))
async def cancel_ord(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, введите id ордера без лишних символов\U0001F194')
    await state.set_state(StepsForm.GET_ORDER)


@dp.message(StepsForm.GET_ORDER)
async def cancel(message: Message, state: FSMContext):
    order_id = message.text
    if order_id:
        order = await cancel_order(category='linear', symbol='BTCUSDT', orderid=order_id, message=message)
        if order['retMsg'] == 'OK':
            await message.answer(f'Заказ с id - {order_id} успешно отменен \U0001F4E8')
        elif order['retMsg'] != 'OK':
            await message.answer('Не удалось отменить заказ, попробуйте снова \U0001F504')
    await state.clear()


@dp.message(Command('set_account'))
async def set_account(message: Message, state: FSMContext):
    await message.answer("Введите тип аккаунта и количество монеты для покупки(не менее 0.001) \U0001F4B3\n"
                         "\n"
                         "Пример: UNIFIED,0.001 \U0000270F\n"
                         "\n"
                         "БЕЗ ПРОБЕЛОВ! \U0000274C")
    await state.set_state(StepsForm.GET_TYPE)


@dp.message(StepsForm.GET_TYPE)
async def get_type(message: Message, state: FSMContext):
    account_qty = message.text.split(',')
    account = account_qty[0]
    qty = float(account_qty[1])

    if qty < 0.001:
        await message.answer('Количество монет должно быть не менее 0.001!')

    elif qty >= 0.001:
        user_id = message.from_user.id

        cur.execute(
            "INSERT OR REPLACE INTO user_account (user_id, account, qty) VALUES (?, ?, ?)",
            (user_id, account, qty)
        )

        conn.commit()
        await message.answer('Благодарю за предоставленные данные! \U0001F60A')

    await state.clear()


@dp.message(Command('check_balance'))
async def check_wallet(message: Message):
    user_id = message.from_user.id

    cur.execute("SELECT account FROM user_account WHERE user_id = ?", (user_id,))
    result = cur.fetchone()

    if result is not None:
        account = result[0]
        if account in ['UNIFIED', 'CONTRACT']:
            totalwalletbalance, availablebalance = check_balance(account)
            await message.answer(f'Ваш баланс: {totalwalletbalance} | USDT \U0001F4B3\n'
                                 f'Доступные средства: {availablebalance} \U0001F4B8')
        else:
            await message.answer('Введите верный тип аккаунта')
    else:
        await message.answer('В базе данных нет вашего id, вызовите команду set_account и повторите попытку \U0001F504')


@dp.message(Command('order_status'))
async def order_status(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, введите id ордера без лишних символов\U0001F194')
    await state.set_state(StepsForm.GET_ID)


@dp.message(StepsForm.GET_ID)
async def get_order_status(message: Message, state: FSMContext):
    order_id = message.text
    if order_id:
        order = get_orders('linear', 'BTCUSDT', order_id)
        if order['result']['list'][0]['orderStatus'] == 'Filled':
            await message.answer(f"Получил данные ордера: \U00002139\n"
                                 f" - Валютная пара: {order['result']['list'][0]['symbol']} \U0001F4B1\n"
                                 f" - ID Ордера: {order['result']['list'][0]['orderId']} \U0001F194\n"
                                 f" - Цена открытия ордера: {order['result']['list'][0]['price']} \U0001F4B5\n"
                                 f" - Количество купленной монеты: {order['result']['list'][0]['qty']} \U0001F4C4\n"
                                 f" - Статус ордера: Исполнен \U00002705\n")
        else:
            await message.answer(f"Получил данные ордера: \U00002139\n"
                                 f" - Валютная пара: {order['result']['list'][0]['symbol']} \U0001F4B1\n"
                                 f" - ID Ордера: {order['result']['list'][0]['orderId']} \U0001F194\n"
                                 f" - Цена открытия ордера: {order['result']['list'][0]['price']} \U0001F4B5\n"
                                 f" - Количество купленной монеты: {order['result']['list'][0]['qty']} \U0001F4C4\n"
                                 f" - Статус ордера: Не исполнен\n")
    else:
        await message.answer("Пожалуйста, введите id ордера без пробелов и лишних символов \U0000270F")
    await state.clear()


@dp.message(Command('trading_info'))
async def get_all_orders(message: Message):
    orders = get_orders('linear', 'BTCUSDT')
    with open('orders.txt', 'w', encoding='utf-8') as temp_file:
        for order in orders['result']['list']:
            if order['orderStatus'] == 'Filled':
                temp_file.write(f"Получил данные ордера: \n"
                                f" - Валютная пара: {order['symbol']} \n"
                                f" - ID Ордера: {order['orderId']} \n"
                                f" - Цена открытия ордера: {order['price']} \n"
                                f" - Количество купленной монеты: {order['qty']} \n"
                                f" - Статус ордера: Исполнен \n"
                                f"\n")
            else:
                temp_file.write(f"Получил данные ордера: \n"
                                f" - Валютная пара: {order['symbol']} \n"
                                f" - ID Ордера: {order['orderId']} \n"
                                f" - Цена открытия ордера: {order['price']} \n"
                                f" - Количество купленной монеты: {order['qty']} \n"
                                f" - Статус ордера: Не исполнен\n"
                                f"\n")
    file = FSInputFile(path='../orders.txt', filename='orders.txt')
    await message.answer_document(document=file, caption='Список всех ордеров')

    os.remove('orders.txt')


async def buy_or_sell():
    while True:
        await get_signal(bot)
        time.sleep(3 * 60)


async def main():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_account (
            user_id INTEGER PRIMARY KEY,
            account VARCHAR(255),
            qty INT
        )
    """)

    conn.commit()

    await buy_or_sell()

    await dp.start_polling(bot)
    dp.message.register(get_type, StepsForm.GET_TYPE)
    dp.message.register(get_order_status, StepsForm.GET_ID)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Code's Exited")
