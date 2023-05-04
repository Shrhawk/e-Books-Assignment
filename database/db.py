import sys

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from config import eBOOKS_DATABASE_URL, ASYNC_TEST_eBOOKS_DATABASE_URL

DATABASE_URL = eBOOKS_DATABASE_URL

if 'pytest' in sys.modules:
    DATABASE_URL = ASYNC_TEST_eBOOKS_DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db() -> Session:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()
