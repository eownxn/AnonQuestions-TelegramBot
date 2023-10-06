from aiogram.filters import BaseFilter
from aiogram.types import Message


class AnyDigitsInMsgFilter(BaseFilter):
    def __init__(self, text: str) -> None:
        self.text = text

    async def __call__(self, msg: Message) -> bool:
        return any(char in msg.text for char in '1234567890')
