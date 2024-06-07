from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_ID = State()


class TypeSteps(StatesGroup):
    GET_TYPE = State()
