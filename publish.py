import json
from logging.handlers import RotatingFileHandler
import ssl
from valkey import Valkey, UsernamePasswordCredentialProvider
import logging

from config import load_configuration_file


# LOG RELATED ##################################3
logger = logging.getLogger("publish")
logger.setLevel(logging.DEBUG)

# Create a file handler and set its level to DEBUG
file_handler = RotatingFileHandler(
    "publish.log",
    mode="a",
    maxBytes=5 * 1024 * 1024,
    backupCount=10,
    encoding=None,
    delay=0,
)
file_handler.setLevel(logging.DEBUG)

# Create a console handler and set its level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for both handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# load configuration
CFG = load_configuration_file()


def publish():
    """Publish a message"""

    client = Valkey(
        host=CFG.connection.host,
        port=CFG.connection.port,
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE,
        credential_provider=UsernamePasswordCredentialProvider(
            username=CFG.connection.user, password=CFG.connection.password
        ),
    )

    # Convert to string
    message_str = json.dumps(
        CFG.publish.message
    )  # Convert dict to string representation

    # Publish
    response = client.publish(
        CFG.publish.channel,
        message_str,  # JSON object as a string
        # encoding="utf-8",  # Specify the encoding for the message
    )

    # log result
    if response == 0:
        logger.info(f"Published message, but no subscribers received it on {CFG.publish.channel}")
    else:
        logger.info(f"Message published to {CFG.publish.channel}, received by {response} subscribers")


# Run the publish function
publish()
