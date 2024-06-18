import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from flask import Flask

from config.config import get_config, Config
from eq_informer_async import get_rabbit_connection_channel, start_consuming_rabbit
from admin_app import db
from admin_app.db_model import User
from middleware.mw_flask import FlaskAppMiddleware
from admin_app import create_app
from messages.message_ru import MESSAGE_RU

queue_name = 'earthquake'
cfg = get_config()
bot = Bot(token=cfg.tbbot_cfg.bot_api)
dp = Dispatcher()


async def bot_start_pooling(flask_app:Flask):
    
    flask_app_mw = FlaskAppMiddleware(flask_app=flask_app)
    dp.message.middleware.register(flask_app_mw)

    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start_handler(message:Message, flask_app:Flask):
    await message.answer(MESSAGE_RU['start'])
    with flask_app.app_context():
        if db.session.query(User).filter_by(user_id=message.from_user.id).count()<1:
            user = User(
                user_id=message.from_user.id,
                chat_id=message.chat.id,
                full_name=message.from_user.full_name,
                user_name=message.from_user.username
                )
            db.session.add(user)
            db.session.commit()

@dp.message()
async def echo_handler(message:Message):
    await message.answer(f'You say: {message.text}')
    

async def main():
    # await asyncio.gather(bot_start_pooling(), start_consuming_rabbit())
    flask_app = create_app()

    # loop = asyncio.get_event_loop()

    # task_bot = loop.create_task(bot_start_pooling(flask_app))
    # rabbit_task = loop.create_task(start_consuming_rabbit(flask_app, db, bot))

    # await asyncio.wait([task_bot,rabbit_task])
    await asyncio.gather(
        bot_start_pooling(flask_app),
        start_consuming_rabbit(flask_app, db, bot)
    )


if __name__ == '__main__':
    

    print('bot started')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('run main complete')
        for task in asyncio.Task.all_tasks():
            task.cancel()

        asyncio.gather(*asyncio.Task.all_tasks(), return_exceptions=True)
        loop = asyncio.get_event_loop()
        loop.stop()

