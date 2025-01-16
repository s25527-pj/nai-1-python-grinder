"""

Hand Gesture Recognition Using Neural Networks and Computer Vision  
Author: Maksymilian Mrówka, Maciej Uzarski  

Environment Setup:  
1. Navigate to the directory containing the script:  
   - cd path/to/computer_vision  
2. Install required dependencies:  
   - pip install -r requirements.txt  
3. Run the script:  
   - Execute the script with `python gesture_recognizer.py`  

Description:  
- This script implements a computer vision-based hand gesture recognition system using OpenCV and MediaPipe.  
- The system processes input from a live camera feed to detect hand landmarks and classify predefined hand gestures.  
- Gestures include:  
  1. Fist  
  2. Palm  
  3. OK sign  
  4. Three (index, middle, and thumb extended, with other fingers folded)  
  5. Phone (thumb and pinky extended, other fingers folded)  
  6. Middle finger gesture  
- The classification logic is based on the relative positions of specific hand landmarks detected by MediaPipe.  

Features:  
1. **Landmark Detection**:  
   - MediaPipe identifies 21 landmarks on the user's hand, including fingertips and joints.  
2. **Gesture Classification**:  
   - Gestures are determined by analyzing the positions of fingertips relative to their corresponding joints.  
3. **Real-Time Feedback**:  
   - The system overlays gesture labels and the state of each finger (straight or folded) directly on the live camera feed.  
4. **Interactive Music Control**:  
   - The system interacts with a media player to control music playback based on detected gestures:  
     - "OK" starts playing music.  
     - "Palm" pauses music.  
     - "Three" resumes music playback.  
     - "Middle finger gesture" stops the music.  
5. **Color-Coded Information**:  
   - Gesture labels are displayed in green, while finger states are displayed in red for improved visibility.  

Output:  
- The script displays the detected gesture in real time, alongside the status of each finger.  
- It serves as a foundation for hand gesture-based interaction systems or further research in computer vision and human-computer interaction.  

"""

import cv2
import mediapipe as mp
import pygame

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def detect_gesture_and_fingers(landmarks):
    if not landmarks:
        return "No hand", []

    tips = [4, 8, 12, 16, 20]
    finger_names = ["thumb", "index", "middle", "ring", "pinky"]
    folded = []
    finger_states = []

    for i, tip in enumerate(tips):
        if tip == 4:
            is_folded = landmarks[tip].y >= landmarks[tip - 1].y
        else:
            is_folded = landmarks[tip].y >= landmarks[tip - 2].y

        folded.append(is_folded)
        state = "folded" if is_folded else "straight"
        finger_states.append(f"{finger_names[i]}: {state}")

    if all(folded): 
        gesture = "Fist"
    elif not any(folded): 
        gesture = "Palm"
    elif not folded[0] and folded[1] and folded[2] and folded[3] and folded[4]: 
        gesture = "OK"
    elif not folded[0] and not folded[1] and not folded[2] and folded[3] and folded[4]: 
        gesture = "Three"
    elif not folded[2] and folded[1] and folded[3] and folded[4]:
        gesture = "That's not very nice"
    elif not folded[0] and not folded[4] and folded[1] and folded[2] and folded[3]:
        gesture = "Phone"
    else:
        gesture = "Unknown"

    return gesture, finger_states


cap = cv2.VideoCapture(0)

pygame.mixer.init()
pygame.mixer.music.load("music.mp3")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Couldn't read input from camera")
        break
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            gesture, finger_states = detect_gesture_and_fingers(landmarks)
            
            if gesture == "OK":
                pygame.mixer.music.play()
                
            if gesture == "Palm":
                pygame.mixer.music.pause()
                
            if gesture == "Three":
                pygame.mixer.music.unpause()
                
            elif gesture == "That's not very nice":
                pygame.mixer.music.stop()

            cv2.putText(image, f"Gesture: {gesture}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            for i, state in enumerate(finger_states):
                cv2.putText(image, state, (10, 80 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Gesture recognizer', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
