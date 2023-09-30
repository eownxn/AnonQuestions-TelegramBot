from aiogram.filters import BaseFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message


# from typing import Any, Container
# from magic_filter.magic import MagicFilter, MagicT


class BasedFilter(BaseFilter):
    def __init__(self, text: str) -> None:
        self.text = text

    async def __call__(self, msg: Message) -> bool:
        return any(char in msg.text for char in '1234567890')


class AnswerCallbackFilter(CallbackData, prefix='answer'):
    _text_: str == 'answer'

# abc = CallbackData('answer', 'non_answer')
