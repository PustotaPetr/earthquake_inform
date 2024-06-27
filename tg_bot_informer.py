from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from flask import Flask

from admin_app import db, flask_app
from admin_app.db_model import User
from config import cfg
from messages.message_ru import MESSAGE_RU
from middleware.mw_flask import FlaskAppMiddleware
from rabbit_consumer import fast_stream_app, prepare_fast_stream_context

queue_name = "earthquake"
bot = Bot(token=cfg.tbbot_cfg.bot_api)
dp = Dispatcher()


async def bot_start_pooling(flask_app: Flask):
    flask_app_mw = FlaskAppMiddleware(flask_app=flask_app)
    dp.message.middleware.register(flask_app_mw)

    await dp.start_polling(bot)


@dp.startup()
async def on_startup():
    print("on_startup: bot started")
    global fast_stream_app
    fast_stream_app = await prepare_fast_stream_context(
        app=fast_stream_app, bot=bot, flask_app=flask_app, db=db
    )
    await fast_stream_app.broker.start()


@dp.shutdown()
async def on_shutdown():
    print("on_shutdown: bot stopped")
    await fast_stream_app.broker.close()


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
