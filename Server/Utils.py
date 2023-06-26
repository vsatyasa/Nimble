"""
This file contains utility methods for handling signaling in an Asyncio RTCPeerConnection.
"""

import asyncio
from aiortc import (
    RTCIceCandidate,
    RTCSessionDescription,
)

async def consume_signaling(pc, signaling):
    """
    This method consumes signaling messages from the `signaling` object and takes appropriate action.

    Args:
        pc (Asyncio RTCPeerConnection): The RTCPeerConnection object to use.
        signaling (object): The signaling object to use.

    Returns:
        None
    """

    while True:
        obj = await signaling.receive()

        if isinstance(obj, RTCSessionDescription):
            # Set the remote description on the `pc` object.
            await pc.setRemoteDescription(obj)

            if obj.type == "offer":
                # Send answer
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)
        elif isinstance(obj, RTCIceCandidate):
            # Add the candidate to the `pc` object.
            await pc.addIceCandidate(obj)
        elif obj is BYE:
            print("Exiting")
            break

