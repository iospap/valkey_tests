"""How to subscribe to a Valkey channel using Valkey's pub/sub feature."""

from logging.handlers import RotatingFileHandler
import ssl
from valkey import Valkey, UsernamePasswordCredentialProvider, ConnectionError
from valkey.client import PubSub
import logging

from config import load_configuration_file


# LOG RELATED ##################################3
logger = logging.getLogger("subscribe")
logger.setLevel(logging.DEBUG)

# Create a file handler and set its level to DEBUG
file_handler = RotatingFileHandler(
    "subscribe.log",
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


# HANDLER FOR PSUBSCRIBE
def my_handler(message):
    logger.debug(" Raw message: %s", message)
    # msg = json.loads(message["data"].decode())
    # logger.debug(msg)
    logger.info(f"Message received in channel-> {message['channel'].decode()}")


# LOG MESSAGES
def process_message(message):
    # check message type
    if message["type"] == "psubscribe":
        logger.info(
            f"Subscribed to channels with pattern: {message["channel"].decode()}"
        )
    elif message["type"] == "subscribe":
        logger.info(f"Subscribed to channel: {message["channel"].decode()}")
    elif message["type"] == "pmessage":
        my_handler(message)
    elif message["type"] == "message":
        my_handler(message)


# LOOP
def subscriber_loop(pubsub: PubSub):
    """pubsub infinite loop"""
    while True:
        try:
            for message in pubsub.listen():
                if message:
                    process_message(message)
        except ConnectionError as e:
            logger.error(f"The connection has been closed: {e}")
        except KeyboardInterrupt:
            logger.info(" Key interrupt... ")
            break


#
def main():

    client = Valkey(
        host=CFG.connection.host,
        port=CFG.connection.port,
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE,
        credential_provider=UsernamePasswordCredentialProvider(
            username=CFG.connection.user, password=CFG.connection.password
        ),
        socket_keepalive=True,
    )
    pubsub = client.pubsub()

    if CFG.subscription.pattern:
        # use psubscribe and handler
        pubsub.psubscribe(**{"gamma*": my_handler})
    elif CFG.subscription.channels:
        # use subscribe without handlers
        pubsub.subscribe(CFG.subscription.channels)
    else:
        logger.error(" Either PATTERN or CHANNELS must be set in the CONFIGURATION")
        return

    # enter the loop
    subscriber_loop(pubsub=pubsub)

    # end
    client.close()


# Execute demo
main()
