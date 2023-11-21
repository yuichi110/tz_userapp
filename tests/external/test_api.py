import os
import pytest
import requests
import json

PROTOCOL = os.environ.get("TEST_API_PROTOCOL", "HTTP").lower()
if PROTOCOL not in ["http", "https"]:
    raise ValueError("supported protocol is http and https")
HOST = os.environ.get("TEST_API_HOST", "127.0.0.1")
PORT = int(os.environ.get("TEST_API_PORT", "8000"))
BASE_URL = f"{PROTOCOL}://{HOST}:{PORT}"


@pytest.mark.skip
def test_all():
    session = requests.Session()

    print("test get /api/users")
    response = session.get(f"{BASE_URL}/api/users")
    print(response.text)
    print()

    print("test get /api/users/yuichi")
    response = session.get(f"{BASE_URL}/api/users/yuichi")
    print(response.text)
    print()

    print("test post /api/signin")
    signin_data = {"username_or_email": "yuichi", "password": "p@ssw0rd"}
    response = session.post(f"{BASE_URL}/api/signin", json=signin_data)
    print(response.text)
    print()

    print("test get /api/users/yuichi")
    response = session.get(f"{BASE_URL}/api/users/yuichi")
    print(response.text)
    print()

    print("test delete /api/signin")
    response = session.delete(f"{BASE_URL}/api/signin")
    print(response.text)
    print()

    print("test get /api/users/yuichi")
    response = session.get(f"{BASE_URL}/api/users/yuichi")
    print(response.text)
    print()

    print("test post /api/users")
    signup_data = {
        "username": "tanzu",
        "email": "tanzu@vmware.com",
        "password1": "p@ssw0rd",
        "password2": "p@ssw0rd",
    }
    response = session.post(f"{BASE_URL}/api/users", json=signup_data)
    print(response.text)

    response = session.get(f"{BASE_URL}/api/users")
    print(response.text)


if __name__ == "__main__":
    test_all()
