import asyncio
import ssl
from valkey import Valkey, UsernamePasswordCredentialProvider

from config import CHANNEL, HOST, MESSAGE, PASS, PORT, USER


async def publish():
    """Publish a message to a Redis channel."""
    crdent = UsernamePasswordCredentialProvider(username=USER, password=PASS)

    client = Valkey(
        host=HOST,
        port=PORT,
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE,
        credential_provider=crdent,
    )

    # Ensure the message is a JSON string
    message_str = str(MESSAGE)  # Convert dict to string representation

    # Publish a message to the 'gamma_oo' channel
    response = client.publish(
        CHANNEL,
        message_str,  # JSON object as a string
        encoding="utf-8",  # Specify the encoding for the message
    )
    if not response:
        print("Failed to publish message.")
    else:
        print("Message published successfully.")


# Run the publish function
asyncio.run(publish())
