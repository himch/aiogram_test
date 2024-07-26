import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings


default = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=settings.bot_token.get_secret_value(),
          default=default)

dp = Dispatcher()
logging.basicConfig(level=logging.DEBUG)
