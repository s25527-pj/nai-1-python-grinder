import cv2
import mediapipe as mp

# Inicjalizacja MediaPipe do śledzenia dłoni
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Funkcja rozpoznająca gesty i stan palców
def detect_gesture_and_fingers(landmarks):
    if not landmarks:
        return "No hand", []

    # Wyciągnięcie pozycji palców
    tips = [4, 8, 12, 16, 20]  # Indeksy końcówek palców
    finger_names = ["thumb", "index", "middle", "ring", "pinky"]
    folded = []
    finger_states = []  # Lista stanów każdego palca

    for i, tip in enumerate(tips):
        if tip == 4:  # Kciuk
            is_folded = landmarks[tip].y >= landmarks[tip - 1].y
        else:  # Pozostałe palce
            is_folded = landmarks[tip].y >= landmarks[tip - 2].y

        folded.append(is_folded)
        state = "folded" if is_folded else "straight"
        finger_states.append(f"{finger_names[i]}: {state}")

    # Rozpoznanie gestu
    if all(folded):  # Wszystkie palce zgięte
        gesture = "Fist"
    elif not any(folded):  # Wszystkie palce wyprostowane
        gesture = "Palm"
    elif not folded[0] and folded[1] and folded[2] and folded[3] and folded[4]:  # "OK"
        gesture = "OK"
    elif not folded[0] and not folded[1] and not folded[2] and folded[3] and folded[4]:  # "Three"
        gesture = "Three"
    elif not folded[2] and folded[1] and folded[3] and folded[4]:  # "Three"
        gesture = "That's not very nice"
    else:
        gesture = "Unknown"

    return gesture, finger_states


# Kamera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Couldn't read input from camera")
        break

    # Obróbka obrazu
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Rysowanie punktów dłoni na obrazie
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Wykrywanie gestu i stanu palców
            landmarks = hand_landmarks.landmark
            gesture, finger_states = detect_gesture_and_fingers(landmarks)

            # Wyświetlanie gestu
            cv2.putText(image, f"Gesture: {gesture}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            # Wyświetlanie stanu palców
            for i, state in enumerate(finger_states):
                cv2.putText(image, state, (10, 80 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Gesture recognizer', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Naciśnij 'q', aby wyjść
        break

cap.release()
cv2.destroyAllWindows()
