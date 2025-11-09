import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# === Einstellungen ===
HAND_BOX = 0.55
BASE_SENSITIVITY = 1.0
MAX_SPEED_BOOST = 2.2
CLICK_THRESHOLD = 0.045
PRECISION_THRESHOLD = 0.08
ALPHA_SLOW = 0.1
ALPHA_FAST = 0.45

# === Setup ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()
prev_x, prev_y = 0, 0
clicking = False
frozen_x, frozen_y = None, None

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Zeichne Handbereich
    x1, x2 = int(w * (0.5 - HAND_BOX / 2)), int(w * (0.5 + HAND_BOX / 2))
    y1, y2 = int(h * (0.5 - HAND_BOX / 2)), int(h * (0.5 + HAND_BOX / 2))
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        # Präzisionsmodus (Daumen & Mittelfinger nah)
        precision_mode = np.hypot(thumb.x - middle_finger.x, thumb.y - middle_finger.y) < PRECISION_THRESHOLD

        # Relative Fingerposition
        rel_x = (index_finger.x - (0.5 - HAND_BOX / 2)) / HAND_BOX
        rel_y = (index_finger.y - (0.5 - HAND_BOX / 2)) / HAND_BOX
        rel_x, rel_y = np.clip(rel_x, 0, 1), np.clip(rel_y, 0, 1)

        # Bildschirmkoordinaten
        x = np.interp(rel_x, [0, 1], [0, screen_w])
        y = np.interp(rel_y, [0, 1], [0, screen_h])

        # Bewegung berechnen
        dx, dy = x - prev_x, y - prev_y
        movement = np.hypot(dx, dy)

        # Adaptive Glättung
        alpha = np.interp(movement, [0, 50], [ALPHA_SLOW, ALPHA_FAST])
        alpha = np.clip(alpha, ALPHA_SLOW, ALPHA_FAST)
        speed_boost = np.interp(movement, [0, 100], [1.0, MAX_SPEED_BOOST])
        sensitivity = BASE_SENSITIVITY * speed_boost

        if precision_mode:
            sensitivity = BASE_SENSITIVITY * 0.4
            alpha = ALPHA_SLOW

        # Klick erkennen
        distance = np.hypot(thumb.x - index_finger.x, thumb.y - index_finger.y)
        if distance < CLICK_THRESHOLD:
            if not clicking:
                clicking = True
                pyautogui.click()
                frozen_x, frozen_y = prev_x, prev_y
                cv2.putText(img, 'KLICK!', (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        else:
            clicking = False
            frozen_x, frozen_y = None, None

        # Mausbewegung
        if frozen_x is not None:
            smooth_x, smooth_y = frozen_x, frozen_y
        else:
            smooth_x = prev_x + (x - prev_x) * alpha * sensitivity
            smooth_y = prev_y + (y - prev_y) * alpha * sensitivity

        # Ränder meiden (verhindert FailSafe-Auslösung)
        smooth_x = np.clip(smooth_x, 5, screen_w - 5)
        smooth_y = np.clip(smooth_y, 5, screen_h - 5)

        pyautogui.moveTo(smooth_x, smooth_y)
        prev_x, prev_y = smooth_x, smooth_y

        # Statusanzeige
        if precision_mode:
            cv2.putText(img, 'PRÄZISIONSMODUS', (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)
        else:
            cv2.putText(img, f'Bewegung: {int(movement)} | Boost: {speed_boost:.2f}',
                        (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 255, 200), 2)

    # Am Ende der Schleife, bevor cv2.imshow
    scale = 2.5  # z.B. 1.5 = 150% der Originalgröße
    img_resized = cv2.resize(img, (0, 0), fx=scale, fy=scale)
    cv2.imshow("Adaptive Hand Maussteuerung", img_resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
