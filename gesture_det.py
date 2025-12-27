class GestureDetection:
    OPEN_HAND_THRESHOLD = 0.12
    LEFT_REGION_RATIO = 1 / 3
    RIGHT_REGION_RATIO = 2 / 3

    def is_hand_open(self, hand_landmarks):
        """
        Determines whether the hand is open based on
        thumb-to-finger distances.
        """

        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]

        # Squared distances (more efficient than sqrt)
        thumb_index_dist_sq = (
            (thumb_tip.x - index_tip.x) ** 2 +
            (thumb_tip.y - index_tip.y) ** 2
        )

        thumb_middle_dist_sq = (
            (thumb_tip.x - middle_tip.x) ** 2 +
            (thumb_tip.y - middle_tip.y) ** 2
        )

        threshold_sq = self.OPEN_HAND_THRESHOLD ** 2

        return (
            thumb_index_dist_sq > threshold_sq and
            thumb_middle_dist_sq > threshold_sq
        )

    def get_hand_direction(self, hand_landmarks, frame_width):
        """
        Determines horizontal hand position in the frame.
        """

        wrist_x = hand_landmarks.landmark[0].x * frame_width

        if wrist_x < frame_width * self.LEFT_REGION_RATIO:
            return "Left"
        elif wrist_x > frame_width * self.RIGHT_REGION_RATIO:
            return "Right"
        return "Center"
