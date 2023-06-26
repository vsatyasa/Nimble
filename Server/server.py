import cv2
import numpy as np
import argparse
import asyncio
import logging
import math
import cv2
import ast
from Config import *
from Utils import *
from BallGenerator import BallGenerator
from MovingBallTrack import MovingBallTrack
from av.video.frame import VideoFrame

from aiortc import RTCPeerConnection
from aiortc.contrib.signaling import TcpSocketSignaling


async def run_offer(pc, signaling):
    """
    Function to run the offer and handle the signaling process.

    Args:
        pc (RTCPeerConnection): RTCPeerConnection object.
        signaling (TcpSocketSignaling): TcpSocketSignaling object.

    Returns:
        None
    """
    await signaling.connect()
    
    ballGenerator = BallGenerator()
    pc.addTrack(MovingBallTrack(ballGenerator))
    channel = pc.createDataChannel("chat")

    @channel.on("message")
    def on_message(message):
        """
        Event listener for the data channel message.

        Args:
            message (str): Received message.

        Returns:
            None
        """
        coordinates = ast.literal_eval(message)
        x, y = coordinates[0]
        client_pos = [x, y] 
        current_pos = ballGenerator.get_current_ball_position()
        print("Current Coordinates:", current_pos, 
              "Client Coordinates:", client_pos,  
              "Error:", math.dist(current_pos, client_pos)
            )

    # send offer
    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)

    await consume_signaling(pc, signaling)


logging.basicConfig(level=logging.INFO)

signaling = TcpSocketSignaling(SIGNALING_HOST, SIGNALING_PORT)
pc = RTCPeerConnection()

coro = run_offer(pc, signaling)

# run event loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(coro)
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(pc.close())
    loop.run_until_complete(signaling.close())
