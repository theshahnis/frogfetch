# core/repository.py
import click
from core.base import ArtifactoryManager

class RepositoryManager(ArtifactoryManager):
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
