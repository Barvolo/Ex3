import requests

def test_create_book():
    url = "http://localhost:5001/books"
    payload = {
        "title": "Adventures of Huckleberry Finn",
        "ISBN": "9780520343641",
        "genre": "Fiction"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "ID" in data
    assert len(data["ID"]) > 0

# Add more tests based on the assignment requirements
