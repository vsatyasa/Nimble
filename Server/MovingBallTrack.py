
import cv2
import numpy as np
from aiortc import VideoStreamTrack
from av.video.frame import VideoFrame

## Media AioRTC MediaStreamTrack
class MovingBallTrack(VideoStreamTrack):
    
    kind = "video"
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
