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

    def check_instance_status(self):
        """Checks if the Artifactory instance is reachable (ping endpoint)."""
        try:
            response = self.make_request('/artifactory/api/system/ping')
            if response.status_code == 200 and response.text.strip() == "OK":
                click.echo("✅ Artifactory is reachable.")
            else:
                raise click.ClickException(f"❌ Ping failed: {response.status_code} – {response.text.strip()}")
        except Exception as e:
            raise click.ClickException(f"❗ Instance check failed: {str(e)}")

    def validate_auth_and_url(self):
        """Validates user auth and if hostname is valid and active"""
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

    def list_repositories(self):
        endpoint = '/artifactory/api/repositories'
        response = self.make_request(endpoint)

        if response.status_code == 200:
            repos = response.json()
            click.echo("📦 Repositories:")
            for repo in repos:
                click.echo(f" - {repo.get('key')} ({repo.get('type')})")
        elif response.status_code == 401:
            raise click.ClickException("🔒 Unauthorized – check your token or credentials.")
        else:
            raise click.ClickException(f"❌ Failed to list repositories: {response.status_code}")