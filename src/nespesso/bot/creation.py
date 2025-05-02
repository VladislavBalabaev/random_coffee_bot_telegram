from aiogram import Bot, Dispatcher

from nespesso.core.configs.env_reader import config

bot = Bot(token=config.TELEGRAM_BOT_TOKEN.get_secret_value())

dp = Dispatcher()
