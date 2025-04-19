import base64
import logging

logger = logging.getLogger("frogfetch")

def secure_login(username, password):
    try:
        auth_string = f"{username}:{password}"
        return base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
    except Exception as e:
        logger.error(f"Failed generating encoded auth due to {e}")
        raise