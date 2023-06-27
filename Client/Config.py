import os

"""
This file contains constants for setting up a TCP connection for signaling.

The `SIGNALING_HOST` constant specifies the host of the TCP server.

The `SIGNALING_PORT` constant specifies the port of the TCP server.
"""

SIGNALING_HOST = "localhost"
SIGNALING_PORT = 8080


## Display ##
## By Default, Display is True
## When running inside the docker container, set Display to False since it doesnt have display
DISPLAY = True
if "Display" in os.environ and os.environ["Display"] == "0":
    DISPLAY = False