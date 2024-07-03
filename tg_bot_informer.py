from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.types import Message, ErrorEvent
from flask import Flask

from admin_app import db, flask_app
from admin_app.db_model import User
from config import cfg
from logger.logger import logger, logger_wraps
from messages.message_ru import MESSAGE_RU
from middleware.bot_middleware import FlaskAppMiddleware, LoggerMiddleware
from rabbit_consumer import fast_stream_app, prepare_fast_stream_context

queue_name = "earthquake"
bot = Bot(token=cfg.tbbot_cfg.bot_api)
dp = Dispatcher()


@logger_wraps()
async def bot_start_pooling(flask_app: Flask):
    login_middleware = LoggerMiddleware(logger)
    dp.message.middleware.register(FlaskAppMiddleware(flask_app=flask_app))
    dp.message.middleware.register(login_middleware)
    dp.error.middleware.register(login_middleware)

    await dp.start_polling(bot)


@logger_wraps()
@dp.startup()
async def on_startup():
    logger.info("on_startup: bot started")
    global fast_stream_app
    fast_stream_app = await prepare_fast_stream_context(
        app=fast_stream_app, bot=bot, flask_app=flask_app, db=db
    )
    await fast_stream_app.broker.start()


@logger_wraps()
@dp.shutdown()
async def on_shutdown():
    logger.info("on_shutdown: bot stopped")
    await fast_stream_app.broker.close()


@dp.error()
async def error_handler(event: ErrorEvent, logger):
    print("!!!!!!!!!!!!!!!!! ERROR !!!!!!!!!!")
    logger.error(event.exception)



@dp.message(CommandStart())
async def command_start_handler(message: Message, flask_app: Flask, logger):
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
            logger.info(
                f"add new user: user_id={message.from_user.id}, full_name={message.from_user.full_name})"
            )


@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"You say: {message.text}")
