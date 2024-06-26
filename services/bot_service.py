from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from flask_sqlalchemy import SQLAlchemy

from messages.message_ru import MESSAGE_RU
from admin_app.db_model import User


async def delete_user(db:SQLAlchemy, user: User):
        print("delete {user=}")
        db.session.delete(user)
        db.session.commit()

async def send_earthqueke_message_to_user(bot: Bot, db:SQLAlchemy, user: User, mq_message_json: dict):
    try:
        await bot.send_message(
            chat_id=user.chat_id,
            text=MESSAGE_RU["earhtqueqe_inform"].format(
                mq_message_json["description"],
                mq_message_json["latitude"],
                mq_message_json["longitude"],
                mq_message_json["depth"],
                mq_message_json["magnitude"],
                mq_message_json["time"],
            ),
        )
        await bot.send_location(
            chat_id=user.chat_id,
            latitude=mq_message_json["latitude"],
            longitude=mq_message_json["longitude"],
        )
    except TelegramForbiddenError:
        await delete_user(db, user)