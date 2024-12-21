from app.database.models import User, Words
from app.database.models import async_session
from sqlalchemy import select, update, delete, desc

start_w = [
    ["Red", "Красный"],
    ["Blue", "Синий"],
    ["Green", "Красный"],
    ["I", "Красный"],
    ["You", "Красный"],
    ["They", "Красный"],
    ["House", "Красный"],
    ["Cat", "Красный"],
    ["Run", "Бежать"],
    ["Happy", "Счастливый"],
]

async def user(tg_id):
  async with async_session() as session:
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
      session.add(User(tg_id=tg_id))
      await session.commit()
      user = await session.scalar(select(User.id).where(User.tg_id == tg_id))
      for i in start_w:
        await session.add(Words(eng=i[0], rus=i[1], user=user))
      await session.commit()

async def get_words(tg_id):
  async with async_session() as session:
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    words = await session.scalars(select(Words).where(Words.user == user.id))
    return words

async def set_words(tg_id, words):
  async with async_session() as session:
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    check_repeat = await session.scalars(select(Words.eng).where(Words.eng == words[0]))
    if check_repeat:
      return 'Такое слово уже есть'
    else:
      session.add(Words(eng=words[0], rus=words[1], user=user.id))
      await session.commit()

async def delete_words(words_id):
  async with async_session() as session:
    await session.execute(delete(Words).where(Words.id == words_id))
    await session.commit()

async def check_words(tg_id, word_question, user_answer):
  async with async_session() as session:
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    words = await session.scalar(select(Words.rus).where(Words.eng == word_question))
    if words == user_answer:
      return True
    else:
      return False