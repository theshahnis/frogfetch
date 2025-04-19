import click
from utils import get_headers, get_logger
from core.system import SystemManager

logger = get_logger("frogfetch")

@click.command()
@click.option('--url', required=True, help='Artifactory base URL')
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
def system_health(url, token, username, password):
    """Check system health of the Artifactory instance via ping."""
    try:
        headers = get_headers(token, username, password)
        manager = SystemManager(url, headers)
        manager.check_instance_status()

    except click.ClickException as ce:
        click.secho(f"[ERROR] {str(ce)}", fg="red")

    except Exception as e:
        logger.exception("Unhandled error in system_health command")
        raise click.ClickException(f"Unexpected error: {str(e)}")

@click.command()
@click.option('--url', required=True, help='Artifactory base URL')
@click.option('--token', help='Bearer token')
@click.option('--username', help='Username for basic auth')
@click.option('--password', help='Password for basic auth')
def dry_run(url, token, username, password):
    """Check connectivity and authentication to Artifactory."""
    try:
        logger.info("🔐 Starting dry-run health check...")
        headers = get_headers(token, username, password)
        manager = SystemManager(url, headers)
        if manager.validate_connection():
            click.echo("✅ Got correct response from hostname")

    except click.ClickException as ce:
        click.secho(f"[ERROR] {str(ce)}", fg="red")

    except Exception as e:
        logger.exception("Unhandled error in dry_run command")
        raise click.ClickException(f"Unexpected error: {str(e)}")