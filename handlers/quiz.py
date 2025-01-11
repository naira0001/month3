# quiz.py
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
import os



async def quiz_1(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    button = InlineKeyboardButton('Далее', callback_data='button1')

    keyboard.add(button)

    question = 'RM or Barcelona'
    answer = ['RM', 'Barcelona', 'Оба']

    await bot.send_poll(
        chat_id=message.chat.id,    # Куда отправить
        question=question,          # Сам вопрос
        options=answer,             # Ответы
        is_anonymous=False,         # Анонимный или нет
        type='quiz',                # Тип опросника
        correct_option_id=2,        # Правильный ответ
        explanation='Жаль...',      # Подсказка
        open_period=60,             # Время работы опросника
        reply_markup=keyboard       # Добавление кнопки
    )

async def quiz_2(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    button = InlineKeyboardButton('Далее', callback_data='button2')

    keyboard.add(button)

    question = 'Dota2 or CS.GO'
    answer = ['Dota2', 'CS.GO']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=1,
        explanation='Эх ты...',
        open_period=60,
        reply_markup = keyboard
    )

async def quiz_3(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    button = InlineKeyboardButton('Далее', callback_data='button3')

    keyboard.add(button)

    question = 'Backend or Frontend'
    answer = ['Backend', 'Frontend']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        explanation='Эх ты :(...',
        open_period=60,
        reply_markup=keyboard
    )

async def quiz4(message: types.Message):


    # Путь к фото
    photo_path = os.path.join('media', 'img1.png')

    # Загружаем фото
    with open(photo_path, 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo)

    # Вопрос викторины
    question = "Какая планета самая большая в Солнечной системе?"
    answers = ["Земля", "Юпитер", "Марс"]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type="quiz",
        correct_option_id=1,
        explanation=" Юпитер",
        open_period=120
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text='button1')
    dp.register_callback_query_handler(quiz_3, text='button2')
    dp.register_callback_query_handler(quiz4)