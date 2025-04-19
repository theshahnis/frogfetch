import click
from utils import get_headers
from core.repository import RepositoryManager
from utils import get_logger

logger = get_logger("frogfetch")

@click.command()
@click.option('--url', required=True)
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
def list_repos(url, token, username, password):
    """List repositories in Artifactory instance."""
    try:
        headers = get_headers(token, username, password)
        manager = RepositoryManager(url, headers)
        manager.list_repositories()
    except click.ClickException as ce:
        click.secho(f"[ERROR] {str(ce)}", fg="red")

    except Exception as e:
        logger.exception("Unhandled error in dry_run command")
        raise click.ClickException(f"Unexpected error: {str(e)}")

@click.command()
@click.option('--repo', required=True, help='Repository key')
@click.option('--url', required=True)
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
@click.option('--output', help='Optional output file for JSON')
def prepare_edit(repo, url, token, username, password, output):
    """Fetchs a conf file for selected repo before applying changes."""
    headers = get_headers(token, username, password)
    manager = RepositoryManager(url, headers)
    manager.prepare_edit_repo(repo_key=repo, output_file=output)

@click.command()
@click.option('--repo', required=True, help='Repository key')
@click.option('--url', required=True)
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
@click.option('--file', 'file_path', required=False, help='Path to edited JSON file')
def apply_edit(repo, url, token, username, password, file_path):
    """Applies edited repository config from file or <repo-key>-values.json."""
    headers = get_headers(token, username, password)
    manager = RepositoryManager(url, headers)
    manager.apply_edit_repo(repo_key=repo, file_path=file_path)


@click.command()
@click.option('--repo', required=True, help='Repository key to delete')
@click.option('--url', required=True)
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
@click.option('--force', is_flag=True, help='Delete without confirmation prompt')
def delete_repo(repo, url, token, username, password, force):
    """Delete a repository from Artifactory."""
    headers = get_headers(token, username, password)
    manager = RepositoryManager(url, headers)
    manager.delete_repository(repo_key=repo, force=force)