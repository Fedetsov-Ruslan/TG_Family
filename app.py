import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from dotenv import load_dotenv, find_dotenv

from middlewares.db import DataBaseSession
load_dotenv(find_dotenv())

from database.engine import create_db, session_maker,drop_db
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from common.bot_cmds_list import private, group


bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()
dp.include_router(user_group_router)
dp.include_router(user_private_router)

async def on_startup(bot):
 
    await create_db()

async def main():
    dp.startup.register(on_startup)
    dp.update.middleware(DataBaseSession(session_poll=session_maker))
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=group, scope=types.BotCommandScopeAllGroupChats())
    #me = await bot.get_me()
    #BOTNAME = me.username    #имя бота
    #await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) #удалить кноку меню
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())