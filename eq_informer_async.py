import asyncio
import json
from re import U

import aio_pika
from aio_pika import IncomingMessage
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from config.config import get_config, Config
from admin_app.db_model import User
from messages.message_ru import MESSAGE_RU

queue_name = 'earthquake'

class RabbitMessage:
    def __init__(self, flask_app: Flask, db: SQLAlchemy, bot:Bot) -> None:
        self.flask_app = flask_app
        self.db = db
        self.bot = bot
        
    async def __call__(self, message: IncomingMessage):
        async with message.process():
            mq_message_str = message.body.decode()
            mq_message_json = json.loads(mq_message_str)
            with self.flask_app.app_context():
                for row in self.db.session.query(User):
                    await self._send_earthqueke_message_to_user(row, mq_message_json)
                    print(f'{row.user_id=} {row.user_name=} {mq_message_json["description"]=} {mq_message_json["longitude"]=}, {mq_message_json["latitude"]=}')


    async def _send_earthqueke_message_to_user(self,user:User, mq_message_json:dict):
        try:
            await self.bot.send_message(
                chat_id=user.chat_id, 
                text=MESSAGE_RU['earhtqueqe_inform'].format(
                    mq_message_json['description'],
                    mq_message_json['latitude'],
                    mq_message_json['longitude'],
                    mq_message_json['depth'],
                    mq_message_json['magnitude'],
                    mq_message_json['time']
                    )
                )
        except TelegramForbiddenError:
            await self._delete_user(user)


    async def _delete_user(self,user:User):
        print('delete {user=}')
        self.db.session.delete(user)
        self.db.session.commit()


async def get_rabbit_connection_channel(cfg: Config) -> tuple[aio_pika.Connection, aio_pika.Channel]:
    # Create connection
    connection = await aio_pika.connect_robust(
        host=cfg.rabbit_cfg.host,
        port=cfg.rabbit_cfg.port,
        login=cfg.rabbit_cfg.user,
        password=cfg.rabbit_cfg.password,
    )

    # Creating a channel
    channel = await connection.channel()

    return connection, channel



async def start_consuming_rabbit(flask_app: Flask, db: SQLAlchemy, bot:Bot):

    cfg = get_config()

    connection, channel = await get_rabbit_connection_channel(cfg)

    queue = await channel.declare_queue(queue_name, durable=True, auto_delete=False)

    await queue.consume(RabbitMessage(flask_app=flask_app, db=db, bot=bot))

    print('Waiting for messages. To exit, press Ctrl+C')

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()

    # Will block here until the connection is closed

if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(main(loop))
    # finally:
    #     loop.close()
    asyncio.run(start_consuming_rabbit())
