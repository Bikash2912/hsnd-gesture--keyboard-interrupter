# hand_tracking.py
import cv2
import mediapipe as mp


class HandTracker:
    def __init__(
        self,
        static_mode=False,
        max_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.6
    ):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        self.mp_draw = mp.solutions.drawing_utils

    def track_hands(self, frame):
        """
        Processes a BGR frame and returns hand landmark results.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(rgb_frame)

    def draw_landmarks(self, frame, results, draw=True):
        """
        Draws hand landmarks on the frame if enabled.
        """
        if draw and results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame

    def release(self):
        """
        Releases MediaPipe resources.
        """
        self.hands.close()
