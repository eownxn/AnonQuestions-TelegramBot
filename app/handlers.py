from aiogram import Router, F
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart
from aiogram.exceptions import TelegramBadRequest

from app.filters import *
from app.keyboards import *
from app.logging import log

user_router = Router()


class Form(StatesGroup):
    text_: str = State()
    sender_id: int = State()
    id_: int = State()
    cached_id: int = State()


class Form2(StatesGroup):
    text_: str = State()


@user_router.message(F.text.startswith('/start') and BasedFilter(text=F.message.text))
async def get_message(msg: Message, state: FSMContext) -> None:
    try:
        if int(msg.text[7::]) == msg.from_user.id:
            await msg.answer(text=f'⛔️ Извини, но ты не можешь отправить сообщение самому себе')
            raise KeyError
        log(msg=msg)
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


@user_router.callback_query()
async def answer_back(cb: CallbackQuery, state: FSMContext) -> None:
    from main import bot

    new_id = cb.data[7::]

    await state.update_data(id_=new_id)
    await bot.send_message(chat_id=cb.from_user.id,
                           text=f'Отправьте ваш ответ на анонимное сообщение',
                           reply_markup=cancel)
    await state.set_state(Form.text_)


@user_router.message(Form.text_)
async def process_text(msg: Message, state: FSMContext) -> None:
    from main import bot

    log(msg=msg)

    await state.update_data(sender_id=msg.from_user.id, )
    data = await state.get_data()
    print(data)

    try:
        await bot.send_message(chat_id=data['id_'], text=f'📨 Получено новое сообщение:\n\n{msg.text}',
                               reply_markup=InlineKeyboardMarkup(
                                   inline_keyboard=new_message_inline_kb(str(msg.from_user.id))))
        await msg.answer(text='Сообщение успешно отправлено!',
                         reply_markup=ReplyKeyboardRemove())

    except TelegramBadRequest:
        await msg.answer(text='Не удалось отправить сообщение этому пользователю!')

    await state.clear()


@user_router.message(CommandStart())
async def start(msg: Message) -> None:
    log(msg=msg)
    await msg.answer(text=f'🔗 Вот твоя личная ссылка:\n\n' +
                          f't.me/an0nym0us_questi0ns_bot?start={msg.from_user.id}\n\n' +
                          f'Опубликуй её и получай анонимные сообщения')


@user_router.message()
async def idk(msg: Message) -> None:
    await msg.answer('Я не знаю такого!')
