import cv2
import numpy as np
import pytest

from BallDetector import BallDetector


class TestBallDetector:
    @pytest.fixture
    def ball_detector(self):
        return BallDetector()

    def test_detect_ball(self, ball_detector):
        # Create a sample frame with a ball
        frame = np.zeros((400, 400, 3), dtype=np.uint8)
        cv2.circle(frame, (200, 200), 20, (0, 0, 255), -1)

        ball_coordinates = ball_detector.detect_ball(frame)

        assert isinstance(ball_coordinates, list)
        assert len(ball_coordinates) == 1
        assert isinstance(ball_coordinates[0], tuple)
        assert len(ball_coordinates[0]) == 2
        assert all(isinstance(coord, int) for coord in ball_coordinates[0])

    def test_detect_ball_no_ball(self, ball_detector):
        # Create a sample frame without a ball
        frame = np.zeros((400, 400, 3), dtype=np.uint8)

        ball_coordinates = ball_detector.detect_ball(frame)

        assert isinstance(ball_coordinates, list)
        assert len(ball_coordinates) == 0


if __name__ == "__main__":
    pytest.main()
