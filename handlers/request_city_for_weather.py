from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
import aiopywttr
from aiohttp import ClientResponseError

from misc import dp


class RequestCity(StatesGroup):
    input_city = State()


@dp.message(StateFilter(None), Command("weather"))
async def cmd_weather(message: Message, state: FSMContext):
    await message.answer(text="Введите название города, в котором вы хотите узнать погоду, "
                              "или нажмите /cancel для отмены:")
    await state.set_state(RequestCity.input_city)


@dp.message(RequestCity.input_city)
async def show_weather(message: Message, state: FSMContext):
    try:
        language = aiopywttr.Language.RU
        weather = await aiopywttr.get_weather(message.text.replace(' ', '+'), language)
        await message.answer(f"Текущая температура: {weather.weather[0].avgtemp_c} °С")
        await state.clear()
    except ClientResponseError:
        await message.answer(
            text="Не удалось найти такой населенный пункт.\n"
                 "Пожалуйста, попробуйте еще раз или нажмите /cancel для отмены:"
        )
