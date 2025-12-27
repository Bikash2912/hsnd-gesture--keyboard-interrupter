import cv2
import pyautogui
import time
from Trackhand import HandTracker
from Detect_Gestures import GestureDetection

tracker = HandTracker()
gesture = GestureDetection()

cap = cv2.VideoCapture(0)

HAND_OPEN = "open"
HAND_CLOSED = "closed"

DIR_LEFT = "left"
DIR_RIGHT = "right"
DIR_CENTER = "center"

current_hand_state = None
current_direction = DIR_CENTER

last_action_time = time.time()
COOLDOWN = 0.2
TARGET_FPS = 60

def press_key(active_key, release_keys=()):
    pyautogui.keyDown(active_key)
    for key in release_keys:
        pyautogui.keyUp(key)

def release_keys(*keys):
    for key in keys:
        pyautogui.keyUp(key)

def cooldown_elapsed(current_time):
    return (current_time - last_action_time) > COOLDOWN

while True:
    frame_start = time.time()

    success, img = cap.read()
    if not success:
        print("Camera read failed")
        break

    results = tracker.track_hands(img)
    img = tracker.draw_landmarks(img, results)

    current_time = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            is_hand_open = gesture.is_hand_open(hand_landmarks)
            hand_direction = gesture.get_hand_direction(
                hand_landmarks, img.shape[1]
            )

            if cooldown_elapsed(current_time):
                if is_hand_open and current_hand_state != HAND_OPEN:
                    press_key('w', release_keys=('s',))
                    current_hand_state = HAND_OPEN
                    last_action_time = current_time

                elif not is_hand_open and current_hand_state != HAND_CLOSED:
                    press_key('s', release_keys=('w',))
                    current_hand_state = HAND_CLOSED
                    last_action_time = current_time


            if cooldown_elapsed(current_time):
                if hand_direction == "Left" and current_direction != DIR_LEFT:
                    press_key('a', release_keys=('d',))
                    current_direction = DIR_LEFT
                    last_action_time = current_time

                elif hand_direction == "Right" and current_direction != DIR_RIGHT:
                    press_key('d', release_keys=('a',))
                    current_direction = DIR_RIGHT
                    last_action_time = current_time

                elif hand_direction == "Center" and current_direction != DIR_CENTER:
                    release_keys('a', 'd')
                    current_direction = DIR_CENTER


            hand_state_text = "Hand Open" if is_hand_open else "Hand Closed"
            cv2.putText(
                img,
                hand_state_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0) if is_hand_open else (0, 0, 255),
                2
            )

            cv2.putText(
                img,
                hand_direction,
                (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2
            )

    cv2.imshow("Hand Tracking", img)

    # -------- FPS Control -------- #
    elapsed = time.time() - frame_start
    time.sleep(max(1 / TARGET_FPS - elapsed, 0))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

