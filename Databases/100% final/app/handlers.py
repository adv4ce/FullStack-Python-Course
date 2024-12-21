from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from . import keyboards as kb
from .database import requests as rq
from .states import Ans
import random as rand
import numpy as np

r = Router()


@r.message(CommandStart())
async def start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(
        f"Привет, {message.from_user.full_name}!\n👋 Я твой помощник для изучения английских слов! 🌟\n🎯 Цель простая: помочь тебе выучить английский легко и интересно. Давай начинать! 😊",
        reply_markup=kb.main,
    )


@r.message(F.text == "Профиль ⚙️")
async def profile(message: Message):
    await message.answer(
        f"👤 Ученик: {message.from_user.first_name}\n\n🆔 ID: {message.from_user.id}\n\n🔢 Кол-во твоих слов: {len([i for i in await rq.get_words(message.from_user.id)])}",
        reply_markup=kb.back,
    )

@r.message(F.text == 'Назад 🔙')
async def back(message: Message):
    await message.answer(f"Чем ты хочешь заняться, {message.from_user.first_name}? 😊", reply_markup=kb.main)
    
@r.message(F.text == 'Мои слова 📓')
async def my_words(message: Message):
    await message.answer('Твои слова 📓', reply_markup=await kb.words_quantity(message.from_user.id))

@r.callback_query(F.data == 'add')
async def add_word(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(Ans.word_eng)
    await callback.message.edit_text('Введи слово на английском')

@r.message(Ans.word_eng)
async def add_eng_word(message: Message, state: FSMContext):
    await state.update_data(word_eng=message.text)
    await state.set_state(Ans.word_rus)
    await message.reply('Введи слово на русском')

@r.message(Ans.word_rus)
async def add_rus_word(message: Message, state: FSMContext):
    await state.update_data(word_rus=message.text)
    data = await state.get_data()
    check = await rq.set_words(message.from_user.id, [data[i] for i in data.keys()])
    if check:
        await message.answer(f'Слово: {data['word_eng']} уже есть в твоей коллекции')
    else:
        await message.answer(f'Слово {data['word_eng']} добавлено')
        await message.answer(f'Твои слова', reply_markup=await kb.words_quantity(message.from_user.id))
    await state.clear()

@r.callback_query(F.data.startswith('word_'))
async def word_info(callback: CallbackQuery, state: FSMContext):
    word = await rq.get_word_info(callback.from_user.id, callback.data.split('_')[1].strip())
    await callback.message.edit_text(f'{word[0]} -> {word[1]}', reply_markup=kb.word_info)
    await state.set_state(Ans.current_word)
    await state.update_data(current_word=word[0])

@r.callback_query(F.data == 'delete')
async def delete_info(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await rq.delete_words(callback.from_user.id, data['current_word'])
    await callback.message.edit_text(f'Слово: {data['current_word']} удалено')
    await state.clear()
    await callback.message.answer(f'Твои слова', reply_markup=await kb.words_quantity(callback.from_user.id))

@r.callback_query(F.data == 'back')
async def delete_info(callback: CallbackQuery):
    await callback.message.edit_text(f'Твои слова', reply_markup=await kb.words_quantity(callback.from_user.id))

async def ask_question(message: Message, state: FSMContext):
    all_words = await rq.get_words(message.from_user.id)
    all_words = list(all_words)
    random_word = all_words[rand.randint(0, len(all_words) - 1)][0]
    await state.set_state(Ans.question)
    await state.update_data(question=random_word)
    await message.answer(f'Как переводится слово 🌍:\n{random_word} 🔤', reply_markup=await kb.learning(message.from_user.id, random_word))
    await state.set_state(Ans.user_answer)

@r.message(Ans.user_answer)
async def add_rus_word(message: Message, state: FSMContext):
    await state.update_data(user_answer=message.text)
    data = await state.get_data()
    check = await rq.check_rus_answer(message.from_user.id, data['question'], data['user_answer'])
    if check:
        await message.answer(f"Правильный ответ! ✅\n{data['question']} переводится как: {data['user_answer']} 🌟")
        await state.clear()
    else:
        await message.answer(f"Неправильный ответ 😕. Попробуй снова!")
        await ask_question(message, state)

@r.message(F.text == 'Обучение 📝')
async def start_learning(message: Message, state: FSMContext):
    await message.answer('Переключаюсь в режим обучения 🎓')
    await ask_question(message, state)