from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from flask import Flask

class FlaskAppMiddleware(BaseMiddleware):
    def __init__(self, flask_app:Flask) -> None:
        super().__init__()

        self.flask_app = flask_app

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        data['flask_app'] = self.flask_app
        return await handler(event, data) 