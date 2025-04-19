import click,logging,requests,base64

logger = logging.getLogger("frogfetch")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@click.group()
def cli():
    """A simple CLI tool to interact with Artifactory"""
    pass

@cli.command()
@click.option('--url', required=True, help='Base URL of your Artifactory instance')
@click.option('--token', help='Bearer token for authentication')
@click.option('--username', help='Username for basic auth (optional)')
@click.option('--password', help='Password for basic auth (optional)')
def dry_run(url, token, username, password):
    """
    Checks the credentials and hostname of the Artifactory instance.
    """
    try:
        if not token and not (username and password):
            raise ValueError("You must provide either a token or both username and password.")
            click.ClickException("You must provide either a token or both username and password.")
        if token:
            logger.info("Using token authentication.")
        else:
            logger.info(f"Using basic authentication for user: {username}")
        if token:
            headers = {
                "Authorization": f"Bearer {token}"
            }
        if username and password:
            secure_pass = secure_login(username,password)
            headers = {
                "Authorization": f"Basic {secure_pass}",
                "Content-Type": "application/json"
            }

        logger.info(f"Checking Auth and Artifactory connectivity at: {url}")
        check_artifactory(url,headers)

    except ValueError as ve:
        logger.error(str(ve))
        raise click.ClickException(str(ve))

    except Exception as e:
        logger.exception("Unexpected error occurred")
        raise click.ClickException(f"Unexpected error: {str(e)}")

def check_artifactory(url,headers):
    endpoint = '/artifactory/api/repositories'
    try:
        response = requests.get("https://" + url + endpoint, headers=headers)

        match response.history:
            case [redirect] if redirect.status_code >= 302:
                raise click.ClickException(
                    "❌ Redirect detected – hostname may be incorrect or pointing to a login page.")
            case []:
                # Hostname is accessible, now check response status
                match response.status_code:
                    case 200:
                        logger.info("✅ Connected to Artifactory and authenticated.")
                        click.echo("Connection successful.")
                    case 401:
                        raise click.ClickException("🔒 Unauthorized – Token or credentials are invalid.")
                    case 403:
                        raise click.ClickException("🚫 Forbidden – You don't have access to this resource.")
                    case 404:
                        raise click.ClickException("🔍 Not Found – Check if the endpoint or URL is correct.")
                    case code if 500 <= code < 600:
                        raise click.ClickException("💥 Server error – Artifactory may be down.")
                    case _:
                        raise click.ClickException(
                            f"❗ Unexpected status code: {response.status_code} – {response.text}")
            case _:
                raise click.ClickException("⚠️ Unexpected redirect behavior – investigate further.")

    except requests.exceptions.ConnectionError:
        raise click.ClickException("🔌 Network error: Could not connect to the server.")
    except requests.exceptions.Timeout:
        raise click.ClickException("⏳ Timeout: The server did not respond in time.")
    except requests.exceptions.RequestException as e:
        logger.exception("RequestException occurred")
        raise click.ClickException(f"❗ Request failed: {str(e)}")

def secure_login(username,password):
    try:
        auth_string = f"{username}:{password}"
        encoded_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        return encoded_auth
    except Exception as e:
        logger.error(f"Failed genarting encoded auth due to {e}")


if __name__ == '__main__':
    cli()
