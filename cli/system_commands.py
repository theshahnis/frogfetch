import click
from utils import get_headers, get_logger
from core.system import SystemManager,ArtifactoryManager

logger = get_logger("frogfetch")

@click.command()
@click.option('--url', required=True)
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
def system_health(url, token, username, password):
    """Check system health of Artifactory instance."""
    headers = get_headers(token, username, password)
    manager = SystemManager(url, headers)
    manager.check_instance_status()

@click.command()
@click.option('--url', required=True)
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
def dry_run(url, token, username, password):
    """Check connectivity and authentication to Artifactory."""
    try:
        logger.info("🔐 Starting dry-run health check...")
        headers = get_headers(token, username, password)
        manager = SystemManager(url, headers)
        manager.validate_auth_and_url()

    except click.ClickException as ce:
        click.secho(f"[ERROR] {str(ce)}", fg="red")

    except Exception as e:
        logger.exception("Unhandled error in dry_run command")
        raise click.ClickException(f"Unexpected error: {str(e)}")