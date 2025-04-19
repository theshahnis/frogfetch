import click
import logging
from core import ArtifactoryManager
from utils import secure_login, get_logger
logger = get_logger("frogfetch")

@click.group()
def cli():
    """A CLI tool to interact with Artifactory"""
    pass

@cli.command()
@click.option('--url', required=True)
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
def dry_run(url, token, username, password):
    """Check connectivity and authentication to Artifactory."""
    try:
        logger.info("🔐 Starting dry-run health check...")
        headers = _get_headers(token, username, password)
        manager = ArtifactoryManager(url, headers)
        manager.validate_auth_and_url()

    except click.ClickException as ce:
        click.secho(f"[ERROR] {str(ce)}", fg="red")

    except Exception as e:
        logger.exception("Unhandled error in dry_run command")
        raise click.ClickException(f"Unexpected error: {str(e)}")

@cli.command()
@click.option('--url', required=True)
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
def system_health(url, token, username, password):
    """Check system health of Artifactory instance."""
    headers = _get_headers(token, username, password)
    manager = ArtifactoryManager(url, headers)
    manager.check_instance_status()

@cli.command()
@click.option('--url', required=True)
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
def list_repos(url, token, username, password):
    """List repositories in Artifactory instance."""
    headers = _get_headers(token, username, password)
    manager = ArtifactoryManager(url, headers)
    manager.list_repositories()

def _get_headers(token, username, password):
    if not token and not (username and password):
        raise click.ClickException("Provide either a token or both username/password.")

    if token:
        return {"Authorization": f"Bearer {token}"}
    else:
        encoded = secure_login(username, password)
        return {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json"
        }


if __name__ == '__main__':
    cli()
