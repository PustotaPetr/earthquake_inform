import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from flask import Flask

from admin_app import db
from admin_app.db_model import User
from config import cfg
from messages.message_ru import MESSAGE_RU
from middleware.mw_flask import FlaskAppMiddleware

queue_name = "earthquake"
bot = Bot(token=cfg.tbbot_cfg.bot_api)
dp = Dispatcher()


async def bot_start_pooling(flask_app: Flask):
    flask_app_mw = FlaskAppMiddleware(flask_app=flask_app)
    dp.message.middleware.register(flask_app_mw)

    await dp.start_polling(bot)


@dp.startup()
async def on_startup():
    print("bot started")


@dp.shutdown()
async def on_shutdown():
    print("bot stopped")


@dp.message(CommandStart())
async def command_start_handler(message: Message, flask_app: Flask):
    await message.answer(MESSAGE_RU["start"])
    with flask_app.app_context():
        if db.session.query(User).filter_by(user_id=message.from_user.id).count() < 1:
            user = User(
                user_id=message.from_user.id,
                chat_id=message.chat.id,
                full_name=message.from_user.full_name,
                user_name=message.from_user.username,
            )
            db.session.add(user)
            db.session.commit()


@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"You say: {message.text}")
