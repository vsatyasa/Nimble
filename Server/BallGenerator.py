import cv2
import numpy as np

class BallGenerator:
    """
    Class to generate frames with a moving ball inside a box.
    """

    BOX_SIZE = 400
    BALL_RADIUS = 20
    BALL_COLOR = (0, 0, 255)  # Red color
    SPEED = 2
    
    def __init__(self):
        """
        Initialize the BallGenerator object.
        """
        self.ball_x = 220
        self.ball_y = self.BOX_SIZE // 2
        self.velocity_x = self.SPEED
        self.velocity_y = self.SPEED
    
    def get_next_frame(self):
        """
        Get the next frame with the updated ball position.

        Returns:
            image (numpy.ndarray): Frame image with the ball.
        """
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
        """
        Get the current position of the ball.

        Returns:
            list: List containing the x and y coordinates of the ball.
        """
        return [self.ball_x, self.ball_y]
