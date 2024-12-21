from .session import async_session
from . import start_words as sw
from .models import User, Word
from sqlalchemy import select, update, delete
from sqlalchemy.future import select

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
            for i in sw.w:
                session.add(Word(eng=i[0], rus=i[1], user_id=user_id))
            await session.commit()


async def get_words(tg_id):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        words = await session.execute(
            select(Word.eng, Word.rus).where(Word.user_id == user_id)
        )

        return words


async def get_word_info(tg_id, words):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        word = await session.execute(
            select(Word.eng, Word.rus).where(Word.eng == words, Word.user_id == user_id)
        )

        return [i for w in word for i in w]


async def set_words(tg_id, words):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        check_repeat = await session.scalar(
            select(Word.eng).where(Word.eng == words[0], Word.user_id == user_id)
        )

        if check_repeat:
            return "Такое слово уже есть"

        else:
            session.add(Word(eng=words[0], rus=words[1], user_id=user_id))
            await session.commit()


async def delete_words(tg_id, word_del):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        word_id = await session.scalar(
            select(Word.id).where(Word.eng == word_del, Word.user_id == user_id)
        )
        await session.execute(
            delete(Word).where(Word.id == word_id, Word.user_id == user_id)
        )
        await session.commit()


async def check_rus_answer(tg_id, word_question, user_answer):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        check_word = await session.scalars(
            select(Word.eng, Word.rus).where(
                Word.rus == word_question, Word.user_id == user_id
            )
        )
        right_answer = [w for w in check_word][1]

        return True if right_answer == user_answer else False
