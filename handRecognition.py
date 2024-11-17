import mediapipe as mp
import cv2
import math
import threading

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

stop = 'no'
noteResults = 'not now'
result = {
    'j': 0,
    'k': 0,
    'l': 0,
    'u': 0
}

# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Function to classify the hand gesture
def classify_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

     # Get the landmarks for the fingerdip
    thumb_dip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    index_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    middle_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    ring_dip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
    pinky_dip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP]

    # Get the landmarks for the fingermcp
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]



    thumb_index_dist = calculate_distance(thumb_tip, index_tip)
    index_middle_dist = calculate_distance(index_tip, middle_tip)
    middle_ring_dist = calculate_distance(middle_tip, ring_tip)
    ring_pinky_dist = calculate_distance(ring_tip, pinky_tip)
    
    
    thumb_tip_ring_dip = calculate_distance(thumb_tip, ring_dip)
    ring_dip_mcp = calculate_distance(ring_dip, ring_mcp)
    pinky_dip_mcp = calculate_distance(pinky_dip, pinky_mcp)

    thumb_tip_middle_pip = calculate_distance(thumb_tip, middle_pip)
    thumb_tip_middle_dip = calculate_distance(thumb_tip, middle_dip)
    thumb_tip_index_pip = calculate_distance(thumb_tip, index_pip)
    

    if 0.012 <= thumb_index_dist <= 0.180 and 0.028 <= index_middle_dist <= 0.114 and 0.032 <= middle_ring_dist <= 0.080 and 0.022 <= ring_pinky_dist <= 0.089 and 0.001 <= thumb_tip_middle_pip <= 0.196 and 0.001 <= thumb_tip_middle_dip <= 0.196 and 0.001 <= thumb_tip_index_pip <= 0.146:
        return 'j', "Closed Fist (Rock)"
    if 0.026 <= thumb_index_dist <= 0.300 and 0.007 <= index_middle_dist <= 0.131 and 0.001 <= middle_ring_dist <= 0.126 and 0.016 <= ring_pinky_dist <= 0.219:
        return 'k', "Open Palm (Paper)"
    if 0.017 <= thumb_index_dist <= 0.424 and 0.002 <= index_middle_dist <= 0.337 and 0.019 <= middle_ring_dist <= 0.497 and 0.011 <= ring_pinky_dist <= 0.144 and 0.002 <= thumb_tip_ring_dip <= 0.214 and 0.002 <= ring_dip_mcp <= 0.127 and 0.002 <= pinky_dip_mcp <= 0.144:
        return 'l', "Peace Sign (Sissors)"
    
    return 'u', "Unknown Gesture"

# Function to capture webcam feed and process gestures
def startWebcam():
    global stop, noteResults, result
    capture = cv2.VideoCapture(0)

    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
        while capture.isOpened():
            ret, frame = capture.read()
            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detected_image = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if detected_image.multi_hand_landmarks:
                for hand_lms in detected_image.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_lms, mp_hands.HAND_CONNECTIONS)
                    res, gesture = classify_gesture(hand_lms)

                    if noteResults == 'now' and res != 'u':
                        result[res] += 1
                    elif noteResults == 'now' and res == 'u':
                        result = {'j': 0, 'k': 0, 'l': 0, 'u': 1}
                        break
                    else:
                        result = {'j': 0, 'k': 0, 'l': 0, 'u': 0}

                    cv2.putText(image, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Webcam', image)

            if cv2.waitKey(1) & 0xFF == ord('q') or stop == 'yes':
                print(f"\nStop: {stop}")
                break

    capture.release()
    cv2.destroyAllWindows()

# Function to start webcam in a new thread
def startWebcamThread():
    webcam_thread = threading.Thread(target=startWebcam, daemon=True)
    webcam_thread.start()
