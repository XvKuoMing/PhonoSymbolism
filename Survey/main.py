import asyncio
import logging

from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import StorageKey
from aiogram import Bot
from aiogram.enums import ParseMode
from content.dialog import DIALOG
from content.utils import gen_brands_names
from db.queries import execute_script, check_user
from structures.inline import create_survey
from routers.survey_manager import survey_managed
from middlewares.throttling import ThrottlingMiddleware
from middlewares.anti_spam import AntiSpamMiddleware

import os
from dotenv import load_dotenv
load_dotenv()  # load .env vars


bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
storage = MemoryStorage()  # для такой задачи внутренней памяти хватит
dp = Dispatcher(bot=bot, storage=storage)
dp.message.filter(F.chat.type == "private")  # only private chats are allowed


@dp.message(Command('start'))
async def greetings(message: Message):
    user_name = message.from_user.full_name
    if await check_user(message.chat.id):
        await message.answer(DIALOG['PASS'].format(name=user_name))
    else:
        await message.answer(DIALOG['START'].format(name=user_name))
        brands = await gen_brands_names()
        survey = await create_survey(values=brands.keys(),
                                     key='Q1')
        await message.answer(text=DIALOG['Q1'],
                             reply_markup=survey)
        storage_key = StorageKey(bot_id=bot.id,
                                 chat_id=message.chat.id,
                                 user_id=message.chat.id)
        await dp.storage.update_data(key=storage_key,
                                     data={'brands': brands,
                                           'user_id': message.chat.id,
                                           })  # storing in order to retrieve chosen group


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await execute_script('init.sql')

    dp.include_router(survey_managed)
    dp.message.outer_middleware(AntiSpamMiddleware())
    dp.message.outer_middleware(ThrottlingMiddleware())
    dp.message.outer_middleware(ThrottlingMiddleware())
    await dp.start_polling(bot)


logging.basicConfig(
    filename="info.log",
    filemode='a',
    level=logging.INFO
)
asyncio.run(main())
