import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import settings, COMMANDS
from misc import dp, bot
import handlers
from utils import send_broadcast_messages


async def main():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    hour, minute = settings.send_messages_time.split(':')
    scheduler.add_job(send_broadcast_messages,
                      trigger='cron',
                      hour=hour,
                      minute=minute)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(COMMANDS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


