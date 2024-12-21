from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import app.keyboards as kb
from app.database.requests import delete_words, set_words, get_words, check_words, user
from random import randint

router = Router()

class Add(StatesGroup):
    word_eng = State()
    word_rus = State()
    user_answer = State()
    question = State()
    
@router.message(CommandStart())
async def start(message: Message):
    await user(message.from_user.id)
    await message.answer("Hi", reply_markup=kb.main)


async def ask_and_handle_question(message: Message, state: FSMContext):
    await state.clear()
    word = await get_words(message.from_user.id)
    word = word[randint(0, len(word))]
    await state.update_data(question=word)
    await message.answer(f"Как переводится слово:\n{word[0]}", reply_markup=await kb.learning_keyboard(message.from_user.id))
    await state.set_state(Add.user_answer)
    
@router.message(Add.user_answer)
async def answer(message: Message, state: FSMContext):
    await state.update_data(user_answer=message.text)
    data = await state.get_data()
    check = await check_words(message.from_user.id, data['question'], data['user_answer'])
    if check:
        await message.answer(f'Правильно! Слово {data['question']} значит {data['user_answer']}')
        await ask_and_handle_question(message, state)

    else:
        while not check:
            await ask_and_handle_question(message, state)

    
@router.message(F.text == "Обучение 📝")
async def profile(message: Message, state: FSMContext):
    await message.answer(
        f"Начнем обучение, {message.from_user.first_name}?", reply_markup=await kb.learning_keyboard(message.from_user.id)
    )
    await ask_and_handle_question(message, state)



@router.message(F.text == "Закончить обучение 🔙")
async def profile(message: Message):
    await message.answer(
        f"Чем ты хочешь заняться, {message.from_user.first_name}?", reply_markup=kb.main
    )


@router.message(F.text == "Мои слова 📓")
async def profile(message: Message):
    await message.answer(f"Твои слова", reply_markup=await kb.words_keyboard(message.from_user.id))


@router.message(F.text == "Профиль ⚙️")
async def profile(message: Message):
    await message.answer(
        f"Имя: {message.from_user.first_name}\nID: {message.from_user.id}\nИзученные слова: {len(get_words(message.from_user.id))}",
        reply_markup=kb.back,
    )


@router.message(F.text == "Назад 🔙")
async def profile(message: Message):
    await message.answer(
        f"Чем ты хочешь заняться, {message.from_user.first_name}?", reply_markup=kb.main
    )

@router.callback_query(F.data.startswith('word_'))
async def delete_word(callback: CallbackQuery):
    await delete_word(callback.data.split('_')[1])
    await callback.message.edit_text(f"Твои слова", reply_markup=await kb.words_keyboard(callback.from_user.id))

@router.callback_query(F.data == 'add')
async def call_add_word(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(Add.word_eng)
    await callback.message.edit_text('Введи слово на английском')
    
@router.message(Add.word_eng)
async def add_word(message: Message, state: FSMContext):
    await state.update_data(word_eng=message.text)
    await state.set_state(Add.word_rus)
    await message.reply('Введи слово на русском')
    
@router.message(Add.word_rus)
async def add_word(message: Message, state: FSMContext):
    await state.update_data(word_rus=message.text)
    data = await state.get_data()
    await set_words(message.from_user.id, [data['word_eng'], data['word_rus']])
    await message.answer(f'Слово {data['word_eng']} добавлено')
    await message.answer(f'Твои слова', reply_markup=await kb.words_keyboard(message.from_user.id))
    await state.clear()
