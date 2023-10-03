from datetime import datetime
from aiogram.types import Message, CallbackQuery


def write_file(event: Message | CallbackQuery) -> True:
    with open(f'logs/{datetime.now().strftime("%d-%m")}_log.txt', 'a', encoding='UTF-8') as f:
        if type(event) == Message:
            text = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} @{event.from_user.username} ' + \
                   f'(id{event.from_user.id})\nText: {event.text}\n\n'
        elif type(event) == CallbackQuery:
            text = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} @{event.from_user.username} ' + \
                   f'(id{event.from_user.id})\nText: {event.data}\n\n'
        f.write(text)
        return True


def write_error(text: str, error) -> True:
    with open(f'logs/{datetime.now().strftime("%d-%m")}_log.txt', 'a', encoding='UTF-8') as f:
        f.write(str(f'Bot: {text}\nError: {error}\n\n'))
