from aiogram.types import Message, CallbackQuery

from datetime import datetime as dt


def log(msg: Message | CallbackQuery, *args) -> None:
    text = do_log(msg=msg, *args)

    with open(f'logs/{dt.now().strftime("%d-%m-%Y")}_log.txt', 'a', encoding='UTF-8') as f:
        f.write(text)


def do_log(msg: Message | CallbackQuery, *args) -> str:
    log_text = f'{dt.now().strftime("%d-%m-%Y %H:%M:%S")}\n' \
               f'Message from {msg.from_user.full_name}, @{msg.from_user.username}\n' \
               f'(id: {msg.from_user.id})\n' \
               f'{msg.text}\n\n'

    return log_text
