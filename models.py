from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import JSON, Integer, Column, String, Text

PG_DSN = "postgresql+asyncpg://user:1234@127.0.0.1:5431/netology"
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    class SwapiPeople(Base):
        __tablename__ = "swapi_people"

        id = Column(Integer, primary_key=True)
        birth_year = Column(String)
        eye_color = Column(String)
        films = Column(Text)
        gender = Column(String)
        hair_color = Column(String)
        height = Column(String)
        homeworld = Column(String)
        mass = Column(String)
        name = Column(String)
        skin_color = Column(String)
        species = Column(Text)
        starships = Column(Text)
        vehicles = Column(Text)
