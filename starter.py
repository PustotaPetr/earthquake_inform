import asyncio

from tg_bot_informer import bot_start_pooling
from admin_app import flask_app
from rabbit_consumer import fast_stream_app


async def main():

    await asyncio.gather(
        bot_start_pooling(flask_app),
        fast_stream_app.run()
        # start_consuming_rabbit(flask_app, db, bot)
    )

if __name__ == '__main__': 
    print('starting service')