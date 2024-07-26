import datetime
import pathlib
from PIL import Image

from aiogram import types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext

from config import settings, COMMANDS
from database import add_user
from misc import dp
from utils import print_user_list


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await add_user(message.from_user.id)
    await message.answer("Добро пожаловать в наш бот!\n"
                         "используйте /help для получения списка доступных команд")


@dp.message(Command("cancel"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Хорошо, продолжаем")
    await state.clear()


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Доступные команды:\n\n" +
                         "\n".join(f"/{command.command} - {command.description}" for command in COMMANDS)
                         )


@dp.message(Command("echo"))
async def cmd_echo(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: неправильный формат команды. Пример:\n"
                             "/echo [текст]")
    else:
        await message.answer(command.args)


@dp.message(Command("photo"))
async def cmd_photo(message: types.Message):
    await message.answer('Пришлите, пожалуйста, фото')


@dp.message(F.photo)
async def get_photo(message: types.Message):
    datetime_str = str(datetime.datetime.now()).translate(str.maketrans({' ': '_', ':': '-', '.': '_'}))
    file_name = f"from_user_id_{message.from_user.id}_at_{datetime_str}"
    full_file_name = pathlib.Path(settings.photos_directory, file_name + ".jpg")
    await message.bot.download(file=message.photo[-1].file_id, destination=full_file_name)
    im = Image.open(full_file_name)
    width, height = im.size
    await message.answer(f'Размер вашего фото {width} на {height} пикселей')


@dp.message(Command("users"))
async def cmd_users(message: types.Message):
    await print_user_list(message)
