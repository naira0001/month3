from aiogram import Dispatcher ,types
from config import bot
import random

async def game_dice(message: types.Message):
    dice_random = random.choice(['🎲', '⚽️', '🎰', '🏀', '🎯', '🎳' ])
    await bot.send_dice(chat_id=message.from_user.id, emoji=dice_random)


async def echo_handler(message: types.Message):
   if message.text.lower() == "game":
        await game_dice(message)
   elif message.text.isdigit():  # Проверяем, состоит ли текст только из цифр
        number = int(message.text)
        await message.answer(f"Квадрат числа: {number ** 2}")
   else:
        await message.answer(message.text)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(game_dice, commands=['game_dice'])
    dp.register_message_handler(echo_handler)