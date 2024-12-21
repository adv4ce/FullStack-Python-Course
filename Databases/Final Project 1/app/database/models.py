from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import asyncio

params = {
  "login": "postgres",
  "password": "salemal2006",
  "localhost": "5432",
  "namedb": "final_db_project"
}
DSN = f""

class Base(AsyncAttrs, DeclarativeBase):
  pass

engine = create_async_engine(url=DSN,
                             echo=True)
    
async_session = async_sessionmaker(engine)

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  tg_id = Column(BigInteger)

class Words(Base):
  __tablename__ = "words"
  id = Column(Integer, primary_key=True)
  eng = Column(String(100))
  rus = Column(String(100))
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship(User, backref="users")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
