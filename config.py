from aiogram.types import BotCommand
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, PositiveInt


MAX_MESSAGES_PER_SECOND = 25

COMMANDS = [
    BotCommand(command="start", description="Начать"),
    BotCommand(command="help", description="Помощь"),
    BotCommand(command="echo", description="Эхо"),
    BotCommand(command="photo", description="Определение размеров изображения"),
    BotCommand(command="users", description="Список пользователей"),
    BotCommand(command="select_buttons", description="Инлайн кнопки"),
    BotCommand(command="weather", description="Текущая погода в городе"),
    BotCommand(command="user_info", description="Запрос имени и возраста пользователя"),
]


class Settings(BaseSettings):
    bot_token: SecretStr
    admin_id: PositiveInt
    developer_id: PositiveInt
    send_messages_time: str
    photos_directory: str
    database_file_name: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
