from aiogram.types import Message  # , CallbackQuery

from datetime import datetime as dt


def get_id(msg: Message) -> None:
    with open(file=f'log.txt', mode='w+', encoding='UTF-8') as f:
        if str(msg.from_user.id) not in f.readlines():
            f.write(f'id{str(msg.from_user.id)} @{msg.from_user.username}\n')


def log_msg(msg: Message):
    print(f'{dt.now().strftime("%Y-%m-%d %H:%M:%S")} @{msg.from_user.username}(id{msg.from_user.id})\nText: {msg.text}')


def log_msg_alt():
    pass
