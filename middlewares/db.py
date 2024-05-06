from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

class DataBaseSession(BaseMiddleware):
    def __init__(self, session_poll: async_sessionmaker):
        self.session_poll = session_poll

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str,Any],
    ):
        async with self.session_poll() as session:
            data['session'] = session
            return await handler(event, data)