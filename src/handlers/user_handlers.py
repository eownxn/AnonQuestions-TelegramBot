import dotenv

from aiogram import F, Router
from aiogram.types import (InlineKeyboardMarkup, ReplyKeyboardRemove,
                           CallbackQuery, Message)
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command

from src.filters import AnyDigitsInMsgFilter
from src.handlers.states import Form, Form2
from src.kb_and_cmd import cancel, new_msg_ikb, help_ikb

user_router = Router()
dotenv.load_dotenv('.env')
BOT_USERNAME = dotenv.dotenv_values('.env')['BOT_USERNAME']
OWNER_ID = dotenv.dotenv_values('.env')['OWNER_ID']


@user_router.message(Command('help', prefix='/'))
async def help_command(msg: Message) -> None:
    await msg.answer(text='Что вас интересует?',
                     reply_markup=InlineKeyboardMarkup(inline_keyboard=help_ikb))


@user_router.callback_query(F.data == 'suggest:command')
async def help_inline(cb: CallbackQuery, state: FSMContext) -> None:
    from app import bot
    await bot.send_message(chat_id=cb.from_user.id,
                           text='Сейчас вы можете предложить что-нибудь!')
    await state.set_state(Form2.text_)


@user_router.callback_query(F.data == 'feedback:command')
async def help_inline(cb: CallbackQuery) -> None:
    from app import bot
    await bot.send_message(chat_id=cb.from_user.id,
                           text='Для того, чтобы связаться с владельцем, напишите: @eownxn_dev')


@user_router.message(F.text.startswith('/start') and AnyDigitsInMsgFilter(text=F.message.text))
async def get_message(msg: Message, state: FSMContext) -> None:
    try:
        if int(msg.text[7::]) == msg.from_user.id:
            await msg.answer(text=f'⛔️ Ты не можешь отправить сообщение самому себе!')
            raise KeyError
        await state.update_data(id_=int(msg.text[7::]))
        await msg.answer(text=f'💬Сейчас ты можешь написать сообщение тому человеку, '
                              f'который опубликовал эту ссылку\n\n✍🏻 Напиши своё сообщение:',
                         reply_markup=cancel)

        await state.set_state(Form.text_)

    except ValueError:
        await msg.answer('Я не знаю такого!')
    except KeyError:
        pass


@user_router.message(F.text == "Отмена")
async def cancel_handler(msg: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()

    await msg.answer(text="Вы отменили отправку сообщения!",
                     reply_markup=ReplyKeyboardRemove())


@user_router.message(Form2.text_)
async def get_suggest(msg: Message, state: FSMContext):
    from app import bot

    await bot.send_message(chat_id=OWNER_ID,
                           text=msg.text)

    await msg.reply(text='Спасибо!')
    await state.clear()


@user_router.callback_query()
async def answer_back(cb: CallbackQuery, state: FSMContext) -> None:
    from app import bot

    new_id = cb.data[7::]

    await state.update_data(id_=new_id)
    await bot.send_message(chat_id=cb.from_user.id,
                           text=f'Отправьте ваш ответ на анонимное сообщение',
                           reply_markup=cancel)
    await state.set_state(Form.text_)


@user_router.message(Form.text_)
async def process_text(msg: Message, state: FSMContext) -> None:
    from app import bot

    await state.update_data(sender_id=msg.from_user.id, )
    data = await state.get_data()

    try:
        await bot.send_message(chat_id=data['id_'], text=f'📨 Получено новое сообщение:\n\n{msg.text}',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=new_msg_ikb(str(msg.from_user.id))))
        await msg.answer(text='Сообщение успешно отправлено!',
                         reply_markup=ReplyKeyboardRemove())

    except TelegramBadRequest as ex:
        text = 'Не удалось отправить сообщение этому пользователю!'
        await msg.answer(text=text)
        from src.logging import write_error
        write_error(text=text, error=ex)

    await state.clear()


@user_router.message(CommandStart())
async def start(msg: Message) -> None:
    await msg.answer(text=f'🔗 Вот твоя личная ссылка:\n\n' +
                          f't.me/{BOT_USERNAME}?start={msg.from_user.id}\n\n' +
                          f'Опубликуй её и получай анонимные сообщения')


@user_router.message()
async def idk(msg: Message) -> None:
    await msg.answer('Я не знаю такого!')
