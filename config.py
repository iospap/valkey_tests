from dataclasses import dataclass
import logging
import os
from typing import Dict, List
import yaml


@dataclass
class connectionObject:
    host: str
    port: int
    user: str = None
    password: str = None

    def __post_init__(self):
        try:
            if not self.user:
                self.channel = "default"
        except Exception as e:
            logging.getLogger(__name__).exception(
                f" Error loading connection configuration: {e}"
            )
            quit


@dataclass
class publishObject:
    channel: str = None
    message: Dict = None

    def __post_init__(self):
        try:
            if not self.channel:
                self.channel = "test"
            if not self.message:
                self.message = {
                    "message": "Hello from publisher!",
                    "status": "success",
                    "code": 200,
                    "timestamp": "2009-07-23T12:30:00Z",
                    "details": {"user": "publisher", "action": "publish"},
                }
        except Exception as e:
            logging.getLogger(__name__).exception(
                f" Error loading publish configuration: {e}"
            )
            quit


@dataclass
class subscriptionObject:
    pattern: str = None
    channels: List[str] = None


@dataclass
class config:
    connection: connectionObject
    subscription: subscriptionObject
    publish: publishObject

    def __post_init__(self):
        try:
            if isinstance(self.connection, dict):
                self.connection = connectionObject(**self.connection)
            if isinstance(self.subscription, dict):
                self.subscription = subscriptionObject(**self.subscription)
            if isinstance(self.publish, dict):
                self.publish = publishObject(**self.publish)
        except Exception as e:
            logging.getLogger(__name__).exception(f" Error loading configuration: {e}")
            quit


def load_configuration_file(cfg_name="configuration.yaml") -> config:
    """Load and return configuration object
       "config.yaml" file should be placed in root

    Returns:
       [configuration object]
    """
    if os.path.exists(cfg_name):
        with open(cfg_name, "rt", encoding="utf8") as f:
            return config(**yaml.safe_load(f.read()))
    else:
        raise FileNotFoundError(f" {cfg_name} configuration file not found")
