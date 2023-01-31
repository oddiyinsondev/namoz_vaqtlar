from aiogram.dispatcher.filters.state import State, StatesGroup


class Register(StatesGroup):
    sura = State()
    oyat = State()