# In this code we are training the code in my way. So we are detecting the hand gestures based on the distance of the tracker set by the mediapipe. Thus to accurately finding out the distance values I ran this code for 1 minute. So the while loop will run for 1 minute. And it will capture the distance. For every change in the resut the while loop is iterating. Hence I aggrated the sum of all the iterations (Distances between near fingers). And after 1 minute it gives me accumulated result for distance between nebigouring fingers. Note: For entire one minute I was gesturing only one gesture (like rock, paper, sissors). And graduately changing the distances and style so the test cases will be diverse.

import mediapipe as mp
import cv2
import math
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Initialize webcam capture
capture = cv2.VideoCapture(0)

# Time settings
start_time = time.time()
test_duration = 60  # 1 minute in seconds

# Variables to accumulate sum of distances
thumb_index_sum = 0
index_middle_sum = 0
middle_ring_sum = 0
ring_pinky_sum = 0

# Variable to record the min and max of the distances
thumb_index_min = 1000
index_middle_min = 1000
middle_ring_min = 1000
ring_pinky_min = 1000
thumb_tip_ring_dip_min = 1000
ring_dip_mcp_min = 1000
pinky_dip_mcp_min = 1000

thumb_tip_middle_pip_min = 1000
thumb_tip_middle_dip_min = 1000
thumb_tip_index_pip_min = 1000




thumb_index_max = -1
index_middle_max = -1
middle_ring_max = -1
ring_pinky_max = -1
thumb_tip_ring_dip_max = -1
ring_dip_mcp_max = -1
pinky_dip_mcp_max = -1

thumb_tip_middle_pip_max = -1
thumb_tip_middle_dip_max = -1
thumb_tip_index_pip_max = -1

# Count the number of frames for averaging
frame_count = 0

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while capture.isOpened():
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detected_image = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if detected_image.multi_hand_landmarks:
            for hand_lms in detected_image.multi_hand_landmarks:
                # Draw landmarks and connections
                mp_drawing.draw_landmarks(image, hand_lms, mp_hands.HAND_CONNECTIONS)

                # Get the landmarks for the fingertips
                thumb_tip = hand_lms.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = hand_lms.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                ring_tip = hand_lms.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                pinky_tip = hand_lms.landmark[mp_hands.HandLandmark.PINKY_TIP]
                
                # Get the landmarks for the fingerdip
                thumb_dip = hand_lms.landmark[mp_hands.HandLandmark.THUMB_IP]
                index_dip = hand_lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
                middle_dip = hand_lms.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
                ring_dip = hand_lms.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
                pinky_dip = hand_lms.landmark[mp_hands.HandLandmark.PINKY_DIP]

                # Get the landmarks for the fingermcp
                thumb_mcp = hand_lms.landmark[mp_hands.HandLandmark.THUMB_MCP]
                index_mcp = hand_lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                middle_mcp = hand_lms.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                ring_mcp = hand_lms.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                pinky_mcp = hand_lms.landmark[mp_hands.HandLandmark.PINKY_MCP]


                index_pip = hand_lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
                middle_pip = hand_lms.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
                ring_pip = hand_lms.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
                pinky_pip = hand_lms.landmark[mp_hands.HandLandmark.PINKY_PIP]
                
                # Calculate distances between key landmarks
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

                # Accumulate the distances for averaging later
                thumb_index_sum += thumb_index_dist
                index_middle_sum += index_middle_dist
                middle_ring_sum += middle_ring_dist
                ring_pinky_sum += ring_pinky_dist

                # Update the frame count
                frame_count += 1

                # Update the min and max:
               
                thumb_index_min = min(thumb_index_dist, thumb_index_min)
                index_middle_min = min(index_middle_dist, index_middle_min)
                middle_ring_min = min(middle_ring_dist, middle_ring_min)
                ring_pinky_min = min(ring_pinky_dist, ring_pinky_min)

                thumb_tip_ring_dip_min = min(thumb_tip_ring_dip, thumb_tip_ring_dip_min)
                ring_dip_mcp_min = min(ring_dip_mcp, ring_dip_mcp_min)
                pinky_dip_mcp_min = min(pinky_dip_mcp, pinky_dip_mcp_min)

                thumb_tip_middle_pip_min = min(thumb_tip_middle_dip, thumb_tip_middle_dip_min)
                thumb_tip_middle_dip_min = min(thumb_tip_middle_dip, thumb_tip_middle_dip_min)
                thumb_tip_index_pip_min = min(thumb_tip_index_pip, thumb_tip_index_pip_min)

                thumb_index_max = max(thumb_index_dist, thumb_index_max)
                index_middle_max = max(index_middle_dist, index_middle_max)
                middle_ring_max = max(middle_ring_dist, middle_ring_max)
                ring_pinky_max = max(ring_pinky_dist, ring_pinky_max)

                thumb_tip_ring_dip_max = max(thumb_tip_ring_dip, thumb_tip_ring_dip_max)
                ring_dip_mcp_max = max(ring_dip_mcp, ring_dip_mcp_max)
                pinky_dip_mcp_max = max(pinky_dip_mcp, pinky_dip_mcp_max)

                thumb_tip_middle_pip_max = max(thumb_tip_middle_dip, thumb_tip_middle_dip_max)
                thumb_tip_middle_dip_max = max(thumb_tip_middle_dip, thumb_tip_middle_dip_max)
                thumb_tip_index_pip_max = max(thumb_tip_index_pip, thumb_tip_index_pip_max)

                # Display the distances on the webcam screen
                cv2.putText(image, f"Thumb-Index: {thumb_index_dist:.3f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(image, f"Index-Middle: {index_middle_dist:.3f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(image, f"Middle-Ring: {middle_ring_dist:.3f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(image, f"Ring-Pinky: {ring_pinky_dist:.3f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show the webcam feed with distance values
        cv2.imshow('Webcam', image)

        # Check if the test duration has passed (1 minute)
        if time.time() - start_time >= test_duration:
            # Calculate and print the averages after 1 minute
            thumb_index_avg = thumb_index_sum / frame_count if frame_count != 0 else 0
            index_middle_avg = index_middle_sum / frame_count if frame_count != 0 else 0
            middle_ring_avg = middle_ring_sum / frame_count if frame_count != 0 else 0
            ring_pinky_avg = ring_pinky_sum / frame_count if frame_count != 0 else 0

             # Print Min, Avg, Max distances
            print("\nAverage Distances (after 1 minute):")
            print(f"Thumb-Index: Min = {thumb_index_min:.3f}, Avg = {thumb_index_avg:.3f}, Max = {thumb_index_max:.3f}")
            print(f"Index-Middle: Min = {index_middle_min:.3f}, Avg = {index_middle_avg:.3f}, Max = {index_middle_max:.3f}")
            print(f"Middle-Ring: Min = {middle_ring_min:.3f}, Avg = {middle_ring_avg:.3f}, Max = {middle_ring_max:.3f}")
            print(f"Ring-Pinky: Min = {ring_pinky_min:.3f}, Avg = {ring_pinky_avg:.3f}, Max = {ring_pinky_max:.3f}")

            print(f"Thumb-Tip-Ring-DIP: Min = {thumb_tip_ring_dip_min:.3f}, Max = {thumb_tip_ring_dip_max:.3f}")
            print(f"Ring DIP-MCP: Min = {ring_dip_mcp_min:.3f}, Max = {ring_dip_mcp_max:.3f}")
            print(f"Pinky DIP-MCP: Min = {pinky_dip_mcp_min:.3f}, Max = {pinky_dip_mcp_max:.3f}")

            
            print(f"Thumb-Tip to Middle-PIP: Min = {thumb_tip_middle_pip_min:.3f}, Max = {thumb_tip_middle_pip_max:.3f}")
            print(f"Thumb-Tip to Middle-DIP: Min = {thumb_tip_middle_dip_min:.3f}, Max = {thumb_tip_middle_dip_max:.3f}")
            print(f"Thumb-Tip to Index-PIP: Min = {thumb_tip_index_pip_min:.3f}, Max = {thumb_tip_index_pip_max:.3f}")



            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

capture.release()
cv2.destroyAllWindows()
