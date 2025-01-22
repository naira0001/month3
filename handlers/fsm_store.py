# fsm_store.py
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from db import main_db


class FsmStore(StatesGroup):
    name = State()
    size = State()
    category = State()
    price = State()
    photo = State()
    productid = State()
    infoproduct = State()
    collection = State()
    submit = State()



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
    await message.answer('Введите уникальный ID продукта:')
    await FsmStore.next()


async def process_productid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['productid'] = int(message.text)
    await message.answer('Введите дополнительную информацию о продукте:')
    await FsmStore.next()


async def process_infoproduct(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['infoproduct'] = message.text
        await message.answer('Какая коллекция ?')
        await FsmStore.next()

async def process_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text
        await message.answer('Верные ли данные ?')
        await FsmStore.next()
        await message.answer_photo(photo=data['photo'],
                                   caption=f'Название - {data["name"]}\n'
                                           f'Размер- {data["size"]}\n'
                                           f'Категория- {data["category"]}\n'
                                           f'Стоимость- {data["price"]}\n'
                                           f'ID продукта {data["productid"]}\n'
                                           f'Информация: {data["infoproduct"]}'
                                           f'Коллекция: {data["collection"]}',
                                                reply_markup=buttons.submit)


async def submit(message: types.Message, state: FSMContext):
    if message.text == 'да':
        # Запись в базу
        async with state.proxy() as data:
            await main_db.sql_insert_store(name=data['name'],
                                       size=data['size'],
                                       price=data['price'],
                                       photo=data['photo'],
                                       productid=data['productid']
        )
            await main_db.sql_insert_product_details(
                productid=data['productid'],
                category=data['category'],
                infoproduct=data['infoproduct']
            )
            await main_db.sql_insert_collections(
                collection=data['collection'],
                productid=data['productid']

            )

            await message.answer('Ваши данные в базе', reply_markup=buttons.remove_keyboard)
        await state.finish()
    elif message.text == 'нет':
        await message.answer('Хорошо, отменено!', reply_markup=buttons.remove_keyboard)
        await state.finish()
    else:
        await message.answer('Выберите да или нет')
async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.remove_keyboard)




def register_handlers_fsm_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='отмена', ignore_case=True), state='*')

    dp.register_message_handler(start_fsm_store, commands='store')
    dp.register_message_handler(process_name, state=FsmStore.name)
    dp.register_message_handler(process_size, state=FsmStore.size)
    dp.register_message_handler(process_category, state=FsmStore.category)
    dp.register_message_handler(process_price, state=FsmStore.price)
    dp.register_message_handler(process_photo, state=FsmStore.photo, content_types=['photo'])
    dp.register_message_handler(process_productid, state=FsmStore.productid)
    dp.register_message_handler(process_infoproduct, state=FsmStore.infoproduct)
    dp.register_message_handler(process_collection, state=FsmStore.collection)
    dp.register_message_handler(submit, state=FsmStore.submit)



