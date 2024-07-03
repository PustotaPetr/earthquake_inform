import logging
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from flask_sqlalchemy import SQLAlchemy

from messages.message_ru import MESSAGE_RU
from admin_app.db_model import User
from logger.logger import logger_wraps


@logger_wraps(level=logging.INFO)
async def delete_user(db: SQLAlchemy, user: User):
    print("delete {user=}")
    db.session.delete(user)
    db.session.commit()


@logger_wraps()
def check_fields_in_message(mq_message_json: dict, log: logging.Logger):
    field_list = ["description", "latitude", "longitude", "depth", "magnitude", "time"]
    for field in field_list:
        if field not in mq_message_json:
            log.warning(
                f'In message id={mq_message_json.get('publicID', 'UNKNOWN')} missed field "{field}"'
            )


@logger_wraps()
async def send_earthquake_message_to_user(
    bot: Bot, db: SQLAlchemy, user: User, mq_message_json: dict
):
    try:
        await bot.send_message(
            chat_id=user.chat_id,
            text=MESSAGE_RU["earhtqueqe_inform"].format(
                mq_message_json.get("description", 'UNKNOWN'),
                mq_message_json.get("latitude", 'UNKNOWN'),
                mq_message_json.get("longitude", 'UNKNOWN'),
                mq_message_json.get("depth", 'UNKNOWN'),
                mq_message_json.get("magnitude", 'UNKNOWN'),
                mq_message_json.get("time", 'UNKNOWN'),
            ),
        )
        await bot.send_location(
            chat_id=user.chat_id,
            latitude=mq_message_json["latitude"],
            longitude=mq_message_json["longitude"],
        )
    except TelegramForbiddenError:
        await delete_user(db, user)
