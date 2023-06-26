import cv2

class BallDetector:
    """
    Class for detecting a ball in an image.
    """

    def __init__(self):
        """
        Initialize the BallDetector object.
        """
        self.ball_radius = 20
        self.ball_color_lower = (0, 0, 200) 
        self.ball_color_upper = (50, 50, 255)

    def detect_ball(self, frame):
        """
        Detect the ball in the given frame.

        Args:
            frame (numpy.ndarray): Input frame image.

        Returns:
            list: List of ball coordinates (centroid points) [(x1, y1), (x2, y2), ...].
        """
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
