import base64
import logging
import click

logger = logging.getLogger("frogfetch")

def secure_login(username, password):
    try:
        auth_string = f"{username}:{password}"
        return base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
    except Exception as e:
        logger.error(f"Failed generating encoded auth due to {e}")
        raise

def get_headers(token: str, username: str, password: str) -> dict:
    """
    Builds authentication headers for Artifactory.
    """
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
