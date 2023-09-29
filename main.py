from aiogram import Dispatcher, Bot

from app.handlers import user_router
from config import BOT_TOKEN

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)


async def main() -> None:
    print('Bot started')

    await including_routers()
    await dp.start_polling(bot, skip_updates=True)


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
