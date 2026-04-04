import requests
from typing import Dict, Any, Optional

class APIClient:
    """API client for making HTTP requests to the test API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def login(self, email: str, password: str) -> requests.Response:
        """Simulate login by posting to /posts."""
        url = f"{self.base_url}/posts"
        data = {"title": "login", "body": f"email: {email}, password: {password}", "userId": 1}
        response = self.session.post(url, json=data)
        return response

    def get_users(self, page: int = 1) -> requests.Response:
        """Get users list."""
        url = f"{self.base_url}/users"
        response = self.session.get(url)
        return response

    def get_user(self, user_id: int) -> requests.Response:
        """Get single user."""
        url = f"{self.base_url}/users/{user_id}"
        response = self.session.get(url)
        return response