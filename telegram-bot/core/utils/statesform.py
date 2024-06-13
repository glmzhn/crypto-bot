from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_ID = State()
    GET_TYPE = State()
    GET_ORDER = State()
