import argparse
import asyncio
import logging
import cv2
from Config import *
from Utils import *

from BallRecvTrack import BallRecvTrack
from aiortc import (
    RTCPeerConnection,
)
from aiortc.contrib.media import MediaRelay
from aiortc.contrib.signaling import TcpSocketSignaling


async def run_answer(pc, signaling):
    """
    Run the answer logic for the peer connection.

    Args:
        pc: The RTCPeerConnection instance.
        signaling: The signaling instance.

    """
    await signaling.connect()
    relay = MediaRelay()

    @pc.on("track")
    def on_track(track):
        """
        Handle incoming tracks.

        Args:
            track: The incoming track.
        """
        ballTrack = BallRecvTrack(relay.subscribe(track), None)
        pc.addTrack(ballTrack)
        
        @pc.on("datachannel")
        def on_datachannel(channel):
            """
            Handle incoming data channels.

            Args:
                channel: The incoming data channel.
            """
            print("Data Channel Initiated")
            ballTrack.set_chat_channel(channel)

    await consume_signaling(pc, signaling)


#### Main ####

signaling = TcpSocketSignaling(SIGNALING_HOST, SIGNALING_PORT)
pc = RTCPeerConnection()
logging.basicConfig(level=logging.INFO)


coro = run_answer(pc, signaling)

# run event loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(coro)
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(pc.close())
    loop.run_until_complete(signaling.close())
