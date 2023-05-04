from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import TEST_eBOOKS_DATABASE_URL
from database.db import Base

test_engine = create_engine(TEST_eBOOKS_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


def get_test_db() -> Session:
    try:
        test_db = TestSessionLocal()
        yield test_db
    finally:
        test_db.close()
