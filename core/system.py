# core/system.py
import click
import requests
from core.base import ArtifactoryManager

class SystemManager(ArtifactoryManager):
    def check_instance_status(self):
        try:
            response = self.make_request('/artifactory/api/system/ping')
            if response.status_code == 200 and response.text.strip() == "OK":
                click.echo("✅ Artifactory is reachable.")
            else:
                raise click.ClickException(f"❌ Ping failed: {response.status_code} – {response.text.strip()}")
        except Exception as e:
            raise click.ClickException(f"❗ Instance check failed: {str(e)}")

    def validate_auth_and_url(self):
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
            raise click.ClickException(f"❗ Request failed: {str(e)}")
