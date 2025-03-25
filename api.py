import requests


def get_all_books():
    response = requests.get("http://127.0.0.1:8000/api/books/")
    if response.status_code == 200:
        data = response.json()
        return data
