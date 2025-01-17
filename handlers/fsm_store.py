# fsm_store.py
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons


class FsmStore(StatesGroup):
    name = State()
    size = State()
    category = State()
    price = State()
    photo = State()



async def start_fsm_store(message:types.Message):
    await FsmStore.name.set()
    await message.answer('Напишите название товара:')


async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    kb= types.ReplyKeyboardMarkup()
    b1 = types.KeyboardButton(text = 'S')
    b2 = types.KeyboardButton(text = 'M')
    b3 = types.KeyboardButton(text = 'L')
    kb.add(b1,b2,b3)
    await message.answer('Напишите размер:', reply_markup=kb)
    await FsmStore.next()


async def process_size(message: types.Message, state: FSMContext):
    kb= types.ReplyKeyboardRemove()
    if message.text  in ('S','M','L'):
        async with state.proxy() as data:
            data['size'] = message.text
        await message.answer('Напишите категорию:', reply_markup=kb)
        await FsmStore.next()
    else:
        await message.answer('Выбери размер из кнопок ')


async def process_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await message.answer('Напишите стоимость')
    await FsmStore.next()


async def process_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Добавьте фото ')
    await FsmStore.next()


async def process_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        await message.answer('Верные ли данные ?')
        await message.answer_photo(photo=data['photo'],
                               caption=f'Название - {data["name"]}\n'
                                       f'Размер- {data["size"]}\n'
                                       f'Категория- {data["category"]}\n'
                                       f'Стоимость- {data["price"]}\n')
    await state.finish()




def register_handlers_fsm_store(dp: Dispatcher):
    dp.register_message_handler(start_fsm_store, commands='store')
    dp.register_message_handler(process_name, state=FsmStore.name)
    dp.register_message_handler(process_size, state=FsmStore.size)
    dp.register_message_handler(process_category, state=FsmStore.category)
    dp.register_message_handler(process_price, state=FsmStore.price)
    dp.register_message_handler(process_photo, state=FsmStore.photo, content_types=['photo'])



