from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    text_: str = State()
    sender_id: int = State()
    id_: int = State()
    cached_id: int = State()


class Form2(StatesGroup):
    text_: str = State()
