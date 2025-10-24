import os
import time
import uuid
import requests


BASE_URL = os.getenv('TEST_BASE_URL', 'http://localhost:8000')


def wait_for_service(url: str, timeout: int = 15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url)
            # if we get any response (404 or 200) the service is up
            return True
        except requests.RequestException:
            time.sleep(0.5)
    raise RuntimeError(f"Service not available at {url}")


def test_signup_and_login_flow():
    # ensure service is up
    wait_for_service(f"{BASE_URL}/")

    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "s3cr3t"

    # Signup (JSON body)
    r = requests.post(f"{BASE_URL}/signup", json={"username": username, "password": password})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get('username') == username

    # Login (form data required by OAuth2 password flow)
    r = requests.post(f"{BASE_URL}/login", data={"username": username, "password": password})
    assert r.status_code == 200, r.text
    token = r.json().get('access_token')
    assert token, "no access_token returned"


def test_login_bad_password_returns_401():
    wait_for_service(f"{BASE_URL}/")

    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "right_pw"

    # create user first
    r = requests.post(f"{BASE_URL}/signup", json={"username": username, "password": password})
    assert r.status_code == 200, r.text

    # attempt login with wrong password
    r = requests.post(f"{BASE_URL}/login", data={"username": username, "password": "wrong"})
    assert r.status_code == 401


def run_manual():
    """Run the signup + login flow and print results. Exits with non-zero code on failure.

    This helper allows running the integration test directly with `python test_auth.py`.
    """
    try:
        print(f"Using base URL: {BASE_URL}")
        wait_for_service(f"{BASE_URL}/")

        username = f"manual_{uuid.uuid4().hex[:8]}"
        password = "s3cr3t"

        print("Signing up...", end=" ")
        r = requests.post(f"{BASE_URL}/signup", json={"username": username, "password": password})
        print(r.status_code)
        if r.status_code != 200:
            print("Signup failed:", r.status_code, r.text)
            raise SystemExit(2)

        print("Logging in...", end=" ")
        r = requests.post(f"{BASE_URL}/login", data={"username": username, "password": password})
        print(r.status_code)
        if r.status_code != 200:
            print("Login failed:", r.status_code, r.text)
            raise SystemExit(3)

        token = r.json().get('access_token')
        if not token:
            print("No token returned")
            raise SystemExit(4)

        print("Success! Access token:", token)
        return 0
    except Exception as exc:
        print("Error during manual run:", exc)
        raise


if __name__ == '__main__':
    # allow overriding via env var TEST_BASE_URL
    import sys

    exit_code = run_manual()
    sys.exit(exit_code)
