from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_words
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


async def learning_keyboard(tg_id):
    all_words = await get_words(tg_id)
    keyboard = ReplyKeyboardBuilder()
    answ_words = []
    while len(answ_words) != 4:
        new_word = all_words[r.randint(0, len(all_words))][0]
        if new_word not in answ_words:
            answ_words.append(new_word)

    for w in answ_words:
        keyboard.add(KeyboardButton(text=w))
    keyboard.add(KeyboardButton(text="Закончить обучение 🔙"))


async def words_keyboard(tg_id):
    all_words = await get_words(tg_id)
    keyboard = InlineKeyboardBuilder()
    for w in all_words:
        word = w[0]
        keyboard.add(InlineKeyboardButton(text=word, callback_data=f"word_{word}"))
    keyboard.add(InlineKeyboardButton(text="Добавить слово", callback_data="add"))
    return keyboard.adjust(2).as_markup()
