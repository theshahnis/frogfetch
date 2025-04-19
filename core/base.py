import requests,click
from urllib.parse import urljoin

class ArtifactoryManager:
    def __init__(self, url: str, headers: dict):
        self.url = url
        self.headers = headers

    def make_request(self, endpoint: str):
        full_url = urljoin(f"https://{self.url}", endpoint)
        return requests.get(full_url, headers=self.headers)

    def validate_connection(self):
        """
        Verifies that the hostname is reachable and credentials are valid.
        """
        try:
            response = self.make_request('/artifactory/api/repositories')

            match response.history:
                case [redirect] if redirect.status_code >= 302:
                    raise click.ClickException("❌ Redirect detected – invalid hostname.")
                case []:
                    match response.status_code:
                        case 200:
                            return True
                        case 401:
                            raise click.ClickException("🔒 Unauthorized – invalid token or credentials.")
                        case 403:
                            raise click.ClickException("🚫 Forbidden – insufficient permissions.")
                        case 404:
                            raise click.ClickException("🔍 Not Found – invalid path or repo.")
                        case code if 500 <= code < 600:
                            raise click.ClickException("💥 Server error – Artifactory might be down.")
                        case _:
                            raise click.ClickException(f"❗ Unexpected status: {response.status_code}")
                case _:
                    raise click.ClickException("⚠️ Unexpected redirect behavior – investigate DNS or proxy.")
        except requests.exceptions.ConnectionError:
            raise click.ClickException("🔌 Network error – could not connect to the host.")
        except requests.exceptions.Timeout:
            raise click.ClickException("⏳ Timeout – the server did not respond in time.")
        except requests.exceptions.RequestException as e:
            raise click.ClickException(f"❗ Request failed: {str(e)}")