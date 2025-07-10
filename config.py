### CONFIGURATION #################
HOST = ""
PORT = 0
USER = ""
PASS = ""
#
# SUBSCRIPTION CFG
#       set one of:
PATTERN = None  # psubscribe -> "channel_name:*"
CHANNELS = []  # subscribe  ["main:8453", "channel:pools:8453"]
#
# PUBLISH CFG
CHANNEL = "test" # channel to publish to
MESSAGE = {
        "message": "Hello from publisher!",
        "status": "success",
        "code": 200,
        "timestamp": "2009-07-23T12:30:00Z",
        "details": {"user": "publisher", "action": "publish"},
    }
