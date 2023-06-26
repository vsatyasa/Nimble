
import cv2
import numpy as np
import argparse
import asyncio
import logging
import math
import time
import multiprocessing
import cv2
import ast
import numpy
from av.video.frame import VideoFrame

from aiortc import (
    RTCIceCandidate,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
from aiortc.contrib.signaling import add_signaling_arguments, create_signaling
from aiortc.contrib.signaling import TcpSocketSignaling

class BallGenerator():
    
    ## State for Ball Generator    
    BOX_SIZE = 400
    BALL_RADIUS = 20
    BALL_COLOR = (0, 0, 255)  # Red color
    SPEED = 2
    
    def __init__(self) -> None:
        ## initalize the ball position to random position
        self.ball_x = 220
        self.ball_y = self.BOX_SIZE // 2
        
        ## initalize the ball velocity
        self.velocity_x = self.SPEED
        self.velocity_y = self.SPEED
    
    def get_next_frame(self):
        image = np.zeros((self.BOX_SIZE, self.BOX_SIZE, 3), dtype=np.uint8)
        image.fill(0)
        # Update ball position
        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y

        # Check ball collision with the boundaries of the box
        if self.ball_x <= self.BALL_RADIUS or self.ball_x >= self.BOX_SIZE - self.BALL_RADIUS:
            self.velocity_x *= -1
        if self.ball_y <= self.BALL_RADIUS or self.ball_y >= self.BOX_SIZE - self.BALL_RADIUS:
            self.velocity_y *= -1

        # Draw the ball on the image
        cv2.circle(image, (self.ball_x, self.ball_y), self.BALL_RADIUS, self.BALL_COLOR, -1)
        return image

    def get_current_ball_position(self):
        return [self.ball_x, self.ball_y]

## Media AioRTC MediaStreamTrack
class MovingBallTrack(VideoStreamTrack):
    
    kind = "video"
    FPS = 30
    cnt = 0


    def __init__(self, generator):
        super().__init__()  # don't forget this!
        self.generator = generator

    async def recv(self):
        ## send 1000 images based on FPS

        frame = self.generator.get_next_frame()

        # Resize frame by self.cnt
        ## Re-sizing images so that client can detect the change
        ## not sure on why this is causing bug on the aiortc track library
        frame = cv2.resize(frame, (frame.shape[1] * (self.cnt + 1), frame.shape[0] * (self.cnt + 1)))
        self.cnt += 1
        self.cnt %= 2
        
        pts, time_base = await self.next_timestamp()
        time_base = time_base + 1
        track_frame =  VideoFrame.from_ndarray(frame, format="rgb24")
        track_frame.pts = pts
        track_frame.time_base = time_base
        return track_frame

class BallDetector:
    def __init__(self):
        self.ball_radius =  20
        self.ball_color_lower = (0, 0, 200) 
        self.ball_color_upper = (50, 50, 255)

    def detect_ball(self, frame):
        # Define a mask to segment the ball based on its color
        mask = cv2.inRange(frame, self.ball_color_lower, self.ball_color_upper)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate through the contours and find the ball
        ball_coordinates = []
        for contour in contours:
            # Calculate the contour area and perimeter
            contour_area = cv2.contourArea(contour)
            contour_perimeter = cv2.arcLength(contour, True)

            # Approximate the contour to a polygon
            epsilon = 0.02 * contour_perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Filter contours based on area and circularity
            if contour_area > 100 and len(approx) > 7:
                # Find the bounding rectangle around the contour
                x, y, w, h = cv2.boundingRect(contour)

                # Calculate the centroid of the bounding rectangle
                centroid_x = x + w // 2
                centroid_y = y + h // 2

                ball_coordinates.append((centroid_x, centroid_y))

        return ball_coordinates

class BallRecvTrack(VideoStreamTrack):
    
    kind = "video"
    cnt = 0
    
    def __init__(self, track, chat_channel):
        super().__init__() 
        self.track = track
        self.chat_channel = None
        self.detector = BallDetector()

    def set_chat_channel(self, chat_channel):
        self.chat_channel = chat_channel

    async def recv(self):
        frame = await self.track.recv()
        
        cv_frame = frame.to_ndarray(format="rgb24")
        
        if frame.height == 800 or frame.width == 800:
            cv_frame = cv2.resize(cv_frame, (400, 400))
            
        ball_coordinates = self.detector.detect_ball(cv_frame)
        
        cv2.imshow("frame", cv_frame)
        cv2.waitKey(10)
        if self.chat_channel is not None: 

            print("Sending ball_coordinates", ball_coordinates)            
            self.chat_channel.send(str(ball_coordinates))
        
        ## imshow the frame and print the ball coordinates
        return frame
        

def channel_log(channel, t, message):
    print("channel(%s) %s %s" % (channel.label, t, message))



async def consume_signaling(pc, signaling):
    while True:
        obj = await signaling.receive()

        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)

            if obj.type == "offer":
                # send answer
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)
        elif isinstance(obj, RTCIceCandidate):
            await pc.addIceCandidate(obj)
        elif obj is BYE:
            print("Exiting")
            break


time_start = None

def current_stamp():
    global time_start

    if time_start is None:
        time_start = time.time()
        return 0
    else:
        return int((time.time() - time_start) * 1000000)


async def run_answer(pc, signaling):
    await signaling.connect()
    relay = MediaRelay()

    @pc.on("track")
    def on_track(track):
        ballTrack = BallRecvTrack(relay.subscribe(track), None)
        pc.addTrack(ballTrack)
        
        @pc.on("datachannel")
        def on_datachannel(channel):
            print("Data Channel Iniated")
            ballTrack.set_chat_channel(channel)

    await consume_signaling(pc, signaling)


async def run_offer(pc, signaling):
    await signaling.connect()
    
    ballGenerator = BallGenerator()
    pc.addTrack(MovingBallTrack(ballGenerator))
    channel = pc.createDataChannel("chat")

    ## Message Listener
    ## which gets the ball coordinates from the client
    ## prints the current ball coordinates and client ball coordinates and error
    @channel.on("message")
    def on_message(message):
        
        ## parse the cordinates sent as [(x,y)] from message string
        coordinates = ast.literal_eval(message)

        x, y = coordinates[0]
        client_pos = [x, y] 
        current_pos = ballGenerator.get_current_ball_position()
        print("Current Coordinates: ", current_pos, 
              "Client Coordinates: ", client_pos,  
              "Error", math.dist(current_pos, client_pos)
            )

    # send offer
    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)

    await consume_signaling(pc, signaling)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SERVER ARGS")
    parser.add_argument("role", choices=["offer", "answer"])
    parser.add_argument("--signaling-host", default="localhost", help="Signaling server host")
    parser.add_argument("--signaling-port", type=int, default=8080, help="Signaling server port")

    args = parser.parse_args()


    logging.basicConfig(level=logging.INFO)

    signaling = TcpSocketSignaling(args.signaling_host, args.signaling_port)
    pc = RTCPeerConnection()
    if args.role == "offer":
        coro = run_offer(pc, signaling)
    else:
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



