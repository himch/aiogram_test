from aiogram import types

from misc import dp


# default handler
@dp.message()
async def all_other_messages(message: types.Message):
    """Default handler"""
    if message.content_type == "text":
        await message.answer("Ничего не понимаю!")
    else:
        await message.answer("Зачем тут это?")