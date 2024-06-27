import asyncio

from tg_bot_informer import bot_start_pooling
from admin_app import flask_app


async def main():
    await bot_start_pooling(flask_app)


if __name__ == "__main__":
    print("starting service")
    asyncio.run(main())
