from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.formatting import Text

from database import set_user_info
from misc import dp


class RequestUserNameAndAge(StatesGroup):
    input_user_name = State()
    input_user_age = State()


@dp.message(StateFilter(None), Command("user_info"))
async def cmd_user_info(message: Message, state: FSMContext):
    await message.answer(text="Введите ваше имя или нажмите /cancel для отмены:")
    await state.set_state(RequestUserNameAndAge.input_user_name)


@dp.message(RequestUserNameAndAge.input_user_name)
async def input_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer(
        text="Теперь, пожалуйста, введите ваш возраст (число от 1 до 199) или нажмите /cancel для отмены:"
    )
    await state.set_state(RequestUserNameAndAge.input_user_age)


@dp.message(RequestUserNameAndAge.input_user_age)
async def input_age(message: Message, state: FSMContext):
    try:
        user_age = int(message.text)
        if 1 <= user_age <= 199:
            await state.update_data(user_age=user_age)
            user_data = await state.get_data()
            await set_user_info(message.from_user.id, user_data['user_name'], user_data['user_age'])
            content = Text(
                "Спасибо!\n" 
                f"Ваше имя: {user_data['user_name']}\n" 
                f"Ваш возраст: {user_data['user_age']}"
            )
            await message.answer(**content.as_kwargs())
            await state.clear()
        else:
            raise ValueError
    except ValueError:
        await message.answer(
            text="Неверный возраст.\n"
                 "Пожалуйста, введите ваш возраст как число от 1 до 199 или нажмите /cancel для отмены:"
        )
