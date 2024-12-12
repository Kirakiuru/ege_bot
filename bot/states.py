from aiogram.fsm.state import default_state, State, StatesGroup


class FillName(StatesGroup):
    first_name = State()
    last_name = State()


class FillScore(StatesGroup):
    subject = State()
    score = State()
