import os
from unittest import mock

import pytest
from fastapi.testclient import TestClient

from app import app
from database.db import Base
from tests.database import test_engine


@pytest.fixture(scope='session')
def client():
    Base.metadata.create_all(bind=test_engine)
    with mock.patch.dict(os.environ, {"TESTING": "Testing"}):
        yield TestClient(app)
    Base.metadata.drop_all(bind=test_engine)
