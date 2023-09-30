from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)


# start_kb = [
#    [KeyboardButton(text='/start')],
#    [KeyboardButton(text='/help'), KeyboardButton(text='Обратная связь')]
# ]

def new_message_inline_kb(value: str):
    return [[InlineKeyboardButton(text='📩 Ответить',
                                  callback_data='answer ' + value)]
            ]


cancel_kb = [[KeyboardButton(text='Отмена')]
             ]

cancel = ReplyKeyboardMarkup(keyboard=cancel_kb,
                             resize_keyboard=True)
