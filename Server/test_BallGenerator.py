import cv2
import numpy as np
import pytest

from BallGenerator import BallGenerator


class TestBallGenerator:
    @pytest.fixture
    def ball_generator(self):
        return BallGenerator()

    def test_get_next_frame(self, ball_generator):
        frame = ball_generator.get_next_frame()
        assert isinstance(frame, np.ndarray)
        assert frame.shape == (400, 400, 3)
        assert frame.dtype == np.uint8

    def test_get_current_ball_position(self, ball_generator):
        position = ball_generator.get_current_ball_position()
        assert isinstance(position, list)
        assert len(position) == 2
        assert all(isinstance(coord, int) for coord in position)

    def test_ball_movement(self, ball_generator):
        initial_position = ball_generator.get_current_ball_position()
        ball_generator.get_next_frame()
        new_position = ball_generator.get_current_ball_position()
        assert new_position != initial_position

    def test_ball_boundary_collision(self, ball_generator):
        ball_generator.ball_x = 20
        ball_generator.velocity_x = -2
        ball_generator.get_next_frame()
        assert ball_generator.velocity_x == 2

    def test_ball_frame_consistency(self, ball_generator):
        frame1 = ball_generator.get_next_frame()
        frame2 = ball_generator.get_next_frame()
        assert not np.array_equal(frame1, frame2)



if __name__ == "__main__":
    pytest.main()

