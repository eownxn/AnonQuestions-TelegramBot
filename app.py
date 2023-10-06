import dotenv

from aiogram import Dispatcher, Bot
from aiogram.methods.delete_webhook import DeleteWebhook

from src.handlers.user_handlers import user_router

dp = Dispatcher()
bot = Bot(token=dotenv.dotenv_values(".env")['BOT_TOKEN'])


async def main() -> None:
    print('Bot is ready to work!')

    await bot(DeleteWebhook(drop_pending_updates=True))
    await including_routers()

    await dp.start_polling(bot, skip_updates=True)


#    await set_start_command(bot)


async def including_routers() -> None:
    routers = (user_router,)

    for __router in routers:
        dp.include_router(__router)


if __name__ == '__main__':
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')
