import pytest
from fastapi import status

from models.author import Author
from tests.database import get_test_db


@pytest.fixture
def db_session():
    yield from get_test_db()


def test_get_authors(db_session, client):
    test_author = Author(name="Test Author")
    db_session.add(test_author)
    db_session.commit()

    response = client.get("/api/v1/authors")

    assert response.status_code == status.HTTP_200_OK
    assert any(author["name"] == test_author.name for author in response.json())


def test_get_author(db_session, client):
    test_author = Author(name="Test Author")
    db_session.add(test_author)
    db_session.commit()

    response = client.get(f"/api/v1/authors/{test_author.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == test_author.name


def test_get_author_with_wrong_id(db_session, client):
    test_author = Author(name="Test Author")
    db_session.add(test_author)
    db_session.commit()

    response = client.get(f"/api/v1/authors/test-d64-c8cb-4ee4-9a9a-8d373581f391")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_author(db_session, client):
    test_author_data = {"author_name": "Test Author"}
    response = client.post("/api/v1/authors", params=test_author_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == test_author_data["author_name"]


def test_update_author(db_session, client):
    test_author = Author(name="Test Author")
    db_session.add(test_author)
    db_session.commit()
    test_author_data = {"name": "Updated Test Author"}

    response = client.patch(f"/api/v1/authors/{test_author.id}", json=test_author_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == test_author_data["name"]


def test_update_author_with_wrong_id(db_session, client):
    test_author = Author(name="Test Author")
    db_session.add(test_author)
    db_session.commit()
    test_author_data = {"name": "Updated Test Author"}

    response = client.patch(f"/api/v1/authors/test-d64-c8cb-4ee4-9a9a-8d373581f391", json=test_author_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_author(db_session, client):
    test_author = Author(name="Test Author")
    db_session.add(test_author)
    db_session.commit()

    response = client.delete(f"/api/v1/authors/{test_author.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Author deleted successfully"}


def test_delete_author_with_wrong_id(db_session, client):
    test_author = Author(name="Test Author")
    db_session.add(test_author)
    db_session.commit()

    response = client.delete(f"/api/v1/authors/test-d64-c8cb-4ee4-9a9a-8d373581f391")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
