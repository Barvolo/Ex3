import requests
import pytest

BASE_URL = "http://127.0.0.1:5001/books"

book1 = { "title": "Adventures of Huckleberry Finn", "ISBN": "9780520343641", "genre": "Fiction" }
book2 = { "title": "The Best of Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction" }
book3 = { "title": "Fear No Evil", "ISBN": "9780394558783", "genre": "Biography" }
book4 = { "title": "No such book", "ISBN": "0000001111111", "genre": "Biography" }
book5 = { "title": "The Greatest Joke Book Ever", "ISBN": "9780380798490", "genre": "Jokes" }

book_ids = []


def test_create_books():
    """Test creating three books."""
    for book in [book1, book2, book3]:
        response = requests.post(BASE_URL, json=book)
        assert response.status_code == 201, f"Failed to create book: {book['title']}"
        book_id = response.json().get("ID")
        assert book_id is not None, f"Book ID is missing for book: {book['title']}"
        book_ids.append(book_id)
    
    # Ensure all IDs are unique
    assert len(set(book_ids)) == 3, "Book IDs are not unique"


def test_get_books():
    """Test retrieving all books."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, "Failed to get books"
    books = response.json()
    assert len(books) == 3, f"Expected 3 books, but got {len(books)}"


def test_get_book_by_id():
    """Test retrieving a book by ID."""
    response = requests.get(f"{BASE_URL}/{book_ids[0]}")
    assert response.status_code == 200, "Failed to get the book by ID"
    book_data = response.json()
    assert book_data["authors"] == "Mark Twain", f"Expected author 'Mark Twain', but got '{book_data['authors']}'"


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
    assert response.status_code == 200, f"Failed to update book: {book_id}"


def test_delete_book():
    """Test deleting a book."""
    response = requests.delete(f"{BASE_URL}/{book_ids[1]}")
    assert response.status_code == 200, f"Failed to delete the book with ID: {book_ids[1]}"


def test_get_deleted_book():
    """Test retrieving a deleted book by ID."""
    response = requests.get(f"{BASE_URL}/{book_ids[1]}")
    assert response.status_code == 404, f"Expected 404 for deleted book, but got {response.status_code}"


def test_invalid_isbn():
    """Test creating a book with an invalid ISBN."""
    response = requests.post(BASE_URL, json=book4)
    assert response.status_code in [400, 500], f"Expected 400 or 500, but got {response.status_code}"


def test_invalid_genre():
    """Test creating a book with an invalid genre."""
    response = requests.post(BASE_URL, json=book5)
    assert response.status_code == 422, f"Expected 422 for invalid genre, but got {response.status_code}"



# BASE_URL = "http://localhost:5001/books"

# book6 = {
#     "title": "The Adventures of Tom Sawyer",
#     "ISBN": "9780195810400",
#     "genre": "Fiction"
# }

# book7 = {
#     "title": "I, Robot",
#     "ISBN": "9780553294385",
#     "genre": "Science Fiction"
# }

# book8 = {
#     "title": "Second Foundation",
#     "ISBN": "9780553293364",
#     "genre": "Science Fiction"
# }

# books_data = []


# def test_post_books():
#     books = [book6, book7, book8]
#     for book in books:
#         res = requests.post(BASE_URL, json=book)
#         assert res.status_code == 201
#         res_data = res.json()
#         assert "ID" in res_data
#         books_data.append(res_data)
#         books_data_tuples = [frozenset(book.items()) for book in books_data]
#     assert len(set(books_data_tuples)) == 3


# def test_get_query():
#     res = requests.get(f"{BASE_URL}?authors=Isaac Asimov")
#     assert res.status_code == 200
#     assert len(res.json()) == 2


# def test_delete_book():
#     res = requests.delete(f"{BASE_URL}/{books_data[0]['ID']}")
#     assert res.status_code == 200


# def test_post_book():
#     book = {
#         "title": "The Art of Loving",
#         "ISBN": "9780062138927",
#         "genre": "Science"
#     }
#     res = requests.post(BASE_URL, json=book)
#     assert res.status_code == 201



# def test_get_new_book_query():
#     res = requests.get(f"{BASE_URL}?genre=Science")
#     assert res.status_code == 200
#     res_data = res.json()
#     assert res_data[0]["title"] == "The Art of Loving"