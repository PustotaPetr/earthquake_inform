from aiogram import Bot
from faststream import Context, FastStream, Logger
from faststream.rabbit import RabbitBroker, RabbitQueue
from faststream.security import SASLPlaintext
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from admin_app.db_model import User
from config import cfg
from services.bot_service import send_earthqueke_message_to_user

queue_name = "earthquake"

broker = RabbitBroker(
    host=cfg.rabbit_cfg.host,
    port=cfg.rabbit_cfg.port,
    security=SASLPlaintext(
        username=cfg.rabbit_cfg.user, password=cfg.rabbit_cfg.password
    ),
)
earthquake_queue = RabbitQueue(name=queue_name, durable=True)

fast_stream_app = FastStream(broker=broker)


async def prepare_fast_stream_context(
    app: FastStream, bot: Bot, flask_app: Flask, db: SQLAlchemy
):
    app.context.set_global("bot", bot)
    app.context.set_global("flask_app", flask_app)
    app.context.set_global("db", db)

    return app


@broker.subscriber(earthquake_queue)
async def print_rabbit_message(
    msg, logger: Logger, bot: Bot = Context(), flask_app: Flask = Context(), db: SQLAlchemy = Context()
):
    print(msg)
    with flask_app.app_context():
        for row in db.session.query(User):
            await send_earthqueke_message_to_user(bot, db, row, msg)
            logger.info('{row.user_id=} {row.user_name=} {msg["description"]=} {msg["longitude"]=}, {msg["latitude"]=}')
