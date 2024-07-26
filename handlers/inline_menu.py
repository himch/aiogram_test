from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from misc import dp


CALLBACK_DATA_PREFIX = "select_"
inline_keyboard_data = (("Выбор 1", CALLBACK_DATA_PREFIX + "1"),
                        ("Выбор 2", CALLBACK_DATA_PREFIX + "2"))

inline_keyboard = InlineKeyboardBuilder()
for text, callback_data in inline_keyboard_data:
    inline_keyboard.add(types.InlineKeyboardButton(
        text=text,
        callback_data=callback_data)
    )


@dp.message(Command("select_buttons"))
async def cmd_select_buttons(message: types.Message):
    await message.answer(
        "Сделайте ваш выбор",
        reply_markup=inline_keyboard.as_markup()
    )


@dp.callback_query(F.data.startswith(CALLBACK_DATA_PREFIX))
async def send_random_value(callback: types.CallbackQuery):
    selected = callback.data.split("_")[1]
    await callback.message.answer(f"Вы выбрали Выбор {selected}")
    await callback.answer(show_alert=False)
