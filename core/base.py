# core/base.py
import requests
from urllib.parse import urljoin

class ArtifactoryManager:
    def __init__(self, url: str, headers: dict):
        self.url = url
        self.headers = headers

    def make_request(self, endpoint: str):
        full_url = urljoin(f"https://{self.url}", endpoint)
        return requests.get(full_url, headers=self.headers)
