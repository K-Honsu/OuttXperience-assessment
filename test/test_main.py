import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.models import Book
from database import engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Create a session for testing
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

client=TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    """
    Create a clean database for testing
    """
    Book.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Book.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    """
    Provide a test client for the FastAPI app
    """
    return TestClient(app)


def test_create_book(client, test_db):
    # Test creating a book
    response = client.post(
        "/api/v1/book", json={"id": 1,"title": "Test Book", "author": "Test Author", "year": 2002, "isbn": "jwwnoiwnef"})
    print({"response" : response})
    assert response.json() == {
        "id" : 1,
        "title" : "Test Book",
        "author": "Test Author",
        "year": 2002,
        "isbn": "jwwnoiwnef"
    }
    # print({"data": data})
    # assert data["status"] == True
    # assert "id" in data["data"]
    # assert data["data"]["title"] == "Test Book"
    # assert data["data"]["author"] == "Test Author"


def test_get_all_books(client, test_db):
    # Test getting all books
    response = client.get("/api/v1/book")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == True
    assert isinstance(data["data"], list)


def test_get_single_book(client, test_db):
    # Create a test book
    test_book = Book(title="Test Book", author="Test Author")
    test_db.add(test_book)
    test_db.commit()

    # Test getting a single book
    response = client.get(f"/api/v1/book/{test_book.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == True
    assert data["data"]["title"] == "Test Book"
    assert data["data"]["author"] == "Test Author"


def test_update_single_book(client, test_db):
    # Create a test book
    test_book = Book(title="Test Book", author="Test Author")
    test_db.add(test_book)
    test_db.commit()

    # Test updating a single book
    response = client.put(
        f"/api/v1/book/{test_book.id}", json={"title": "Updated Title"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == True
    assert data["data"]["title"] == "Updated Title"


def test_delete_single_book(client, test_db):
    # Create a test book
    test_book = Book(title="Test Book", author="Test Author")
    test_db.add(test_book)
    test_db.commit()

    # Test deleting a single book
    response = client.delete(f"/api/v1/book/{test_book.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == True
