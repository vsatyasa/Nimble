import cv2
from BallDetector import BallDetector
from aiortc import (
    VideoStreamTrack
)

class BallRecvTrack(VideoStreamTrack):
    """
    A custom video stream track for ball detection and processing.
    """

    kind = "video"
    cnt = 0

    def __init__(self, track, chat_channel):
        """
        Initializes a BallRecvTrack instance.

        Args:
            track: The video stream track to process.
            chat_channel: The chat channel to send ball coordinates.
        """
        super().__init__() 
        self.track = track
        self.chat_channel = None
        self.detector = BallDetector()

    def set_chat_channel(self, chat_channel):
        """
        Sets the chat channel for sending ball coordinates.

        Args:
            chat_channel: The chat channel to set.
        """
        self.chat_channel = chat_channel

    def process_a(self, cv_frame, result_queue):
        """
        Performs ball detection on the given frame.

        Args:
            cv_frame: The OpenCV frame to process.
            result_queue: The multiprocessing queue to store the ball coordinates.

        Returns:
            The detected ball coordinates.
        """
        ball_coordinates = self.detector.detect_ball(cv_frame)
        return ball_coordinates

    async def recv(self):
        """
        Receives and processes video frames from the track.

        Returns:
            The processed frame.
        """
        frame = await self.track.recv()
        
        cv_frame = frame.to_ndarray(format="rgb24")
        if frame.height == 800 or frame.width == 800:
            cv_frame = cv2.resize(cv_frame, (400, 400))

        ball_coordinates = self.process_a(cv_frame, None)
        
        cv2.imshow("frame", cv_frame)
        cv2.waitKey(10)
        
        if self.chat_channel is not None and len(ball_coordinates) > 0: 
            print("Sending ball_coordinates", ball_coordinates)
            self.chat_channel.send(str(ball_coordinates))

        return frame
