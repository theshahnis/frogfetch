import click
from utils import get_headers
from core.repository import RepositoryManager

@click.command()
@click.option('--url', required=True)
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
def list_repos(url, token, username, password):
    """List repositories in Artifactory instance."""
    headers = get_headers(token, username, password)
    manager = RepositoryManager(url, headers)
    manager.list_repositories()
