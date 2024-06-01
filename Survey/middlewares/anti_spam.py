from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from content.dialog import DIALOG
from cachetools import TTLCache


class AntiSpamMiddleware(BaseMiddleware):
    """Checks if users inputt cannot be handled, if it is true, then returns STOP_SPAM message and clears the message"""
    def __init__(self, throttle_time: int = 10):
        self.caches = TTLCache(maxsize=10_000, ttl=throttle_time)

    async def unknown_message(self, message: Message):
        if message.chat.id in self.caches:
            if self.caches[message.chat.id] >= 2 and self.caches[message.chat.id] % 2 == 0:  # на каждое второе сообщение будем кидать предупреждение
                await message.delete()
                await message.answer(text=DIALOG['STOP_SPAM'])
            else:
                self.caches[message.chat.id] += 1
                await message.delete()
        else:
            self.caches[message.chat.id] = 0
            await message.delete()

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        result = await handler(event, data)
        if result is not None:  # that means event is not handled
            return await self.unknown_message(message=event)
        return
