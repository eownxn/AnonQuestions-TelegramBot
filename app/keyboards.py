from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

# start_kb = [
#    [KeyboardButton(text='/start')],
#    [KeyboardButton(text='/help'), KeyboardButton(text='Обратная связь')]
# ]


new_message_inline_kb = [[InlineKeyboardButton(text='📩 Ответить', callback_data='answer')]]

cancel_kb = [[KeyboardButton(text='Отмена')]]

new_message = InlineKeyboardMarkup(inline_keyboard=new_message_inline_kb)
cancel = ReplyKeyboardMarkup(keyboard=cancel_kb,
                             resize_keyboard=True)
