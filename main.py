from aiogram import executor
import logging
from config import bot, Admins, dp
from handlers import commands, echo, quiz, webapp , fsm_store
from buttons import start
from db import main_db

async def on_startup(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text='Бот включен!', reply_markup=start)

    await main_db.create_db()

commands.register_handlers(dp)
quiz.register_handlers(dp)
webapp.register_handlers(dp)
fsm_store.register_handlers_fsm_store(dp)

echo.register_handlers(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)