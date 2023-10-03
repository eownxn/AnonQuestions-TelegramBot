from aiogram import Bot
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup, BotCommand, BotCommandScopeDefault)


def new_msg_ikb(value: str):
    return [[InlineKeyboardButton(text='📩 Ответить',
                                  callback_data='answer ' + value)]]


cancel_kb = [[KeyboardButton(text='Отмена')]]

cancel = ReplyKeyboardMarkup(keyboard=cancel_kb,
                             resize_keyboard=True)

# async def set_start_command(bot: Bot):
#    return await bot.set_my_commands(
#        commands=[
#            BotCommand(command='start', description='Получить ссылку')
#        ],
#        scope=BotCommandScopeDefault()
#    )

help_ikb = [[InlineKeyboardButton(text='📱 Предложить что-нибудь', callback_data='suggest:command')],
            #            [InlineKeyboardButton(text='🚥 Старт', callback_data='start:command')],
            [InlineKeyboardButton(text='✈️ Обратная связь', callback_data='feedback:command')]]
