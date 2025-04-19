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
        if not token and not (username and password):
            raise click.ClickException("Provide either a token or both username/password.")
        if token:
            headers = {"Authorization": f"Bearer {token}"}
        else:
            encoded = secure_login(username, password)
            headers = {"Authorization": f"Basic {encoded}", "Content-Type": "application/json"}

        manager = ArtifactoryManager(url, headers)
        manager.check_connection()

    except click.ClickException as ce:
        click.secho(f"[ERROR] {str(ce)}", fg="red")

    except Exception as e:
        logger.exception("Unhandled error in dry_run command")
        raise click.ClickException(f"Unexpected error: {str(e)}")





if __name__ == '__main__':
    cli()
