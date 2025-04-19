import requests
import click
import logging
from urllib.parse import urljoin

logger = logging.getLogger("frogfetch")

class ArtifactoryManager:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def make_request(self, endpoint: str):
        full_url = urljoin(f"https://{self.url}", endpoint)
        return requests.get(full_url, headers=self.headers)

    def check_connection(self):
        try:
            response = self.make_request('/artifactory/api/repositories')

            match response.history:
                case [redirect] if redirect.status_code >= 302:
                    raise click.ClickException("❌ Redirect detected – invalid hostname.")
                case []:
                    match response.status_code:
                        case 200:
                            click.echo("✅ Authenticated and connected.")
                        case 401:
                            raise click.ClickException("🔒 Unauthorized.")
                        case 403:
                            raise click.ClickException("🚫 Forbidden.")
                        case 404:
                            raise click.ClickException("🔍 Not Found.")
                        case code if 500 <= code < 600:
                            raise click.ClickException("💥 Server error.")
                        case _:
                            raise click.ClickException(f"❗ Unexpected status: {response.status_code}")
                case _:
                    raise click.ClickException("⚠️ Unexpected redirect behavior.")
        except requests.exceptions.ConnectionError:
            raise click.ClickException("🔌 Network error.")
        except requests.exceptions.Timeout:
            raise click.ClickException("⏳ Timeout.")
        except requests.exceptions.RequestException as e:
            logger.exception("RequestException occurred")
            raise click.ClickException(f"❗ Request failed: {str(e)}")