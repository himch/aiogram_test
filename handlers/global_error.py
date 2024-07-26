from aiogram import F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message
import logging

from config import settings
from misc import dp, bot

logger = logging.getLogger(__name__)


@dp.error(ExceptionTypeFilter(Exception), F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: Message):
    await message.answer("Произошла ошибка, попробуйте позже")
    error_message = f"Critical error caused by {event.exception} during chat with telegram id={message.from_user.id}"
    await bot.send_message(settings.developer_id, error_message)
    logger.critical(error_message, exc_info=True)
