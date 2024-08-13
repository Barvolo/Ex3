import requests
import pytest

BASE_URL = "http://localhost:5001/books"
book_ids = []

@pytest.fixture(scope="module")
def setup_teardown():
    """Setup and teardown for the test module."""
    yield
    cleanup_books()

def cleanup_books():
    """Delete all books in the database."""
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        for book in response.json():
            requests.delete(f"{BASE_URL}/{book['ID']}")

def test_create_books():
    """Test creating multiple books."""
    books = [
        {"title": "The Adventures of Tom Sawyer", "ISBN": "9780195810400", "genre": "Fiction"},
        {"title": "I, Robot", "ISBN": "9780553294385", "genre": "Science Fiction"},
        {"title": "Second Foundation", "ISBN": "9780553293364", "genre": "Science Fiction"}
    ]

    for book in books:
        response = requests.post(BASE_URL, json=book)
        assert response.status_code == 201
        response_data = response.json()
        assert "ID" in response_data
        book_ids.append(response_data["ID"])

    # Ensure unique IDs are generated
    assert len(set(book_ids)) == len(books)

def test_get_books():
    """Test retrieving all books."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # Assuming only 3 books have been added so far

def test_get_book_by_id():
    """Test retrieving a single book by its ID."""
    book_id = book_ids[0]
    response = requests.get(f"{BASE_URL}/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Adventures of Tom Sawyer"

def test_update_book():
    """Test updating a book's details."""
    book_id = book_ids[1]
    updated_data = {
        "title": "I, Robot - Updated",
        "ISBN": "9780553294385",
        "genre": "Science Fiction",
        "authors": "Isaac Asimov",
        "publisher": "Spectra",
        "publishedDate": "1991-06-01",
        "ID": book_id
    }
    response = requests.put(f"{BASE_URL}/{book_id}", json=updated_data)
    assert response.status_code == 200

    # Verify the update
    response = requests.get(f"{BASE_URL}/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "I, Robot - Updated"

def test_delete_book():
    """Test deleting a book."""
    book_id = book_ids[2]
    response = requests.delete(f"{BASE_URL}/{book_id}")
    assert response.status_code == 200

    # Verify deletion
    response = requests.get(f"{BASE_URL}/{book_id}")
    assert response.status_code == 404

def test_invalid_isbn():
    """Test handling invalid ISBN."""
    invalid_book = {"title": "Unknown Book", "ISBN": "123456789", "genre": "Fiction"}
    response = requests.post(BASE_URL, json=invalid_book)
    assert response.status_code in [400, 500]  # Depending on how your API handles this case

def test_invalid_genre():
    """Test handling invalid genre."""
    invalid_genre_book = {"title": "Strange Book", "ISBN": "9780553293364", "genre": "Unknown Genre"}
    response = requests.post(BASE_URL, json=invalid_genre_book)
    assert response.status_code == 422  # Assuming 422 is returned for validation errors
