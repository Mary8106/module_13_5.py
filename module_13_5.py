from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ""
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
kb1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

button = KeyboardButton(text='Информация')
button1 = KeyboardButton(text='Рассчитать')

kb.row(button, button1)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    man = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.reply('Привет! Я бот, помогающий вашему здоровью.\n'
                        'Нажмите одну из кнопок для продолжения', reply_markup=kb)

@dp.message_handler(text=['Рассчитать'], state=None)
async def set_age(message: types.Message, state: FSMContext):
    await message.reply('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age_=message.text)
    await message.reply('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth_=message.text)
    await message.reply('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight_=message.text)
    await message.reply('Введите свой пол (м / ж):')
    await UserState.man.set()

@dp.message_handler(state=UserState.man)
async def set_calories(message: types.Message, state: FSMContext):
    await state.update_data(man_=message.text)
    data = await state.get_data()
    if str(data['man_']) == 'м':
        calories = int(data['weight_']) * 10 + int(data['growth_']) * 6.25 - int(data['age_']) * 5 + 5
        await message.reply(f'Ваша норма калорий {calories} в день')
    elif str(data['man_']) == 'ж':
        calories = int(data['weight_']) * 10 + int(data['growth_']) * 6.25 - int(data['age_']) * 5 - 161
        await message.reply(f'Ваша норма калорий {calories} в день')
    await state.finish()

@dp.message_handler(text=['Информация'])
async def inform(message):
    await message.answer("Бот поможет рассчитать суточный рацион в калориях для вашего возраста, роста, веса и пола")

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)