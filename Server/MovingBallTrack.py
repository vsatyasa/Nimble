import cv2
import numpy as np
from aiortc import VideoStreamTrack
from av.video.frame import VideoFrame

class MovingBallTrack(VideoStreamTrack):
    """
    A custom VideoStreamTrack that generates frames with a moving ball.
    """

    kind = "video"
    cnt = 0

    def __init__(self, generator):
        """
        Initialize the MovingBallTrack object.

        Args:
            generator: An instance of the BallGenerator class.
        """
        super().__init__()
        self.generator = generator

    async def recv(self):
        """
        Receive the next frame from the track.

        Returns:
            av.video.frame.VideoFrame: The video frame containing the generated image.
        """

        frame = self.generator.get_next_frame()

        # Resize frame by self.cnt
        frame = cv2.resize(frame, (frame.shape[1] * (self.cnt + 1), frame.shape[0] * (self.cnt + 1)))
        self.cnt += 1
        self.cnt %= 2

        pts, time_base = await self.next_timestamp()
        time_base = time_base + 1
        track_frame = VideoFrame.from_ndarray(frame, format="rgb24")
        track_frame.pts = pts
        track_frame.time_base = time_base
        return track_frame
