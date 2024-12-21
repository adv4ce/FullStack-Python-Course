from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from .database import requests as rq
import numpy as np
import random as r

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Обучение 📝")],
        [KeyboardButton(text="Профиль ⚙️"), KeyboardButton(text="Мои слова 📓")],
    ],
    resize_keyboard=True,
)

back = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Назад 🔙")]],
    resize_keyboard=True,
)

word_info = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Удалить слово 🗑️", callback_data='delete')],
        [InlineKeyboardButton(text="Назад 🔙", callback_data='back')]],
    resize_keyboard=True,
)

async def learning(tg_id, correct_word):
    keyboard = ReplyKeyboardBuilder()
    data = await rq.get_words(tg_id)
    data = list(data)
    words = [data[r.randint(0, len(data) - 1)][1] for i in range(3)]
    correct_word = await rq.get_word_info(tg_id, correct_word)
    words.append(correct_word[1])
    np.random.shuffle(words)
    for i in words:
        keyboard.add(KeyboardButton(text=i))

    keyboard.add(KeyboardButton(text='Закончить обучение 🔙'))
    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard.adjust(2).export(),
        resize_keyboard=True  # Устанавливаем resize
    )
    return keyboard

async def words_quantity(tg_id):
    keyboard = InlineKeyboardBuilder()
    data = await rq.get_words(tg_id)
    for i in data:
        word = i[0]
        keyboard.add(InlineKeyboardButton(text=word, callback_data=f"word_{word}"))
    keyboard.add(InlineKeyboardButton(text="Добавить слово", callback_data="add"))
    return keyboard.adjust(2).as_markup()
