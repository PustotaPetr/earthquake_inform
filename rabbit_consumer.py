from aiogram import Bot
from faststream import Context, FastStream, Logger
from faststream.rabbit import RabbitBroker, RabbitQueue
from faststream.security import SASLPlaintext
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from logger.logger import logger
from config import cfg
from services.bot_service import (
    end_earthquake_message_to_all_user,
    check_fields_in_message,
)

queue_name = "earthquake"


broker = RabbitBroker(
    host=cfg.rabbit_cfg.host,
    port=cfg.rabbit_cfg.port,
    security=SASLPlaintext(
        username=cfg.rabbit_cfg.user, password=cfg.rabbit_cfg.password
    ),
    logger=logger,
)
earthquake_queue = RabbitQueue(name=cfg.rabbit_cfg.queue, durable=True)

fast_stream_app = FastStream(broker=broker)


# broker_logger = broker.logger
# file_handler = logging.FileHandler(os.path.join("logs", cfg.logging.filename))
# file_handler.setFormatter(logging.Formatter(fmt=broker.get_fmt()))
# broker_logger.addHandler(file_handler)


async def prepare_fast_stream_context(
    app: FastStream, bot: Bot, flask_app: Flask, db: SQLAlchemy
):
    app.context.set_global("bot", bot)
    app.context.set_global("flask_app", flask_app)
    app.context.set_global("db", db)

    return app


@broker.subscriber(earthquake_queue)
async def get_rabbit_message(
    msg,
    logger: Logger,
    bot: Bot = Context(),
    flask_app: Flask = Context(),
    db: SQLAlchemy = Context(),
):
    check_fields_in_message(mq_message_json=msg, log=logger)

    with flask_app.app_context():
        await end_earthquake_message_to_all_user(bot, db, msg, logger)
