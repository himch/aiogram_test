import asyncio

from config import settings, MAX_MESSAGES_PER_SECOND
from database import all_users, get_user_info
from misc import bot


async def print_user(tg_id):
    try:
        user_id, name, age = await get_user_info(tg_id)
        user = await bot.get_chat(tg_id)
        full_name = user.first_name + ('' if user.last_name is None else ' ' + user.last_name)
    except Exception:
        name, age = '?', 0
        full_name = '-- утрачен --'

    return f'<a href="tg://user?id={tg_id}">{full_name}</a>, id {tg_id}, name {name[:100]}, age {age if age else "?"}'


async def print_user_list(message):
    await message.answer(f"Список пользователей:")
    async for users_chunk in all_users(chunk_size=MAX_MESSAGES_PER_SECOND):
        for user in users_chunk:
            await message.answer(await print_user(user))
        await asyncio.sleep(1)


async def send_broadcast_messages():
    await bot.send_message(settings.admin_id, "Start sending broadcast messages")
    message_text = "Не забудьте проверить уведомления!"
    async for users_chunk in all_users(chunk_size=MAX_MESSAGES_PER_SECOND):
        for user in users_chunk:
            await bot.send_message(user, message_text)
        await asyncio.sleep(1)

    await bot.send_message(settings.admin_id, "Finish sending broadcast messages")
