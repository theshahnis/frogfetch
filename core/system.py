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

