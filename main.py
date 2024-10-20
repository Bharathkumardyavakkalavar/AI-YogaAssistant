import cv2
import mediapipe as mp
import numpy as np
import threading
import pyttsx3
import time
import queue

# Create a pose instance
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
message_queue = queue.Queue()

# Initialize the text-to-speech engine
engine = pyttsx3.init()
angle_descriptions = ["left wrist", "right wrist", "left elbow", "right elbow", "left shoulder", "right shoulder", "left knee", "right knee", "left ankle", "right ankle", "left hip", "right hip"]
angle_name_list = ["L-wrist","R-wrist","L-elbow", "R-elbow","L-shoulder", "R-shoulder", "L-knee", "R-knee","L-ankle","R-ankle","L-hip", "R-hip"]
angle_coordinates = [[13, 15, 19], [14, 16, 18], [11, 13, 15], [12, 14, 16], [13, 11, 23], [14, 12, 24], [23, 25, 27], [24, 26, 28],[23,27,31],[24,28,32],[24,23,25],[23,24,26]]
correction_value = [15, 15, 30, 30, 30, 30, 30, 30, 30, 30, 40, 50]
accurate_angle_lists = [186.79236959719265,166.43574061364416,141.81039376391257,224.41629249129787,188.52906860618086,174.8638364969756,183.66067668142912,23.693125825515928,188.99720320596475,156.08015257991323,83.09989767223368,146.61052599229896]
# i = None
def calculate_angle(point_a, point_b, point_c):
    radians = np.arctan2(point_c[1] - point_b[1], point_c[0] - point_b[0]) - np.arctan2(point_a[1] - point_b[1], point_a[0] - point_b[0])
    angle = np.degrees(radians)
    return angle + 360 if angle < 0 else angle

def text_to_speech(message_queue):
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    special_message = "Lift your right leg and place it at the inner side of left thigh"
    last_spoken_time = None  # Variable to track the last spoken time of the special message

    while True:
        message = message_queue.get()
        current_time = time.time()

        # if message == special_message:
            # Check if the special message has been spoken recently
        if last_spoken_time is None:
            engine.setProperty('rate', 120)
            time.sleep(1)
            engine.say(special_message)
            engine.runAndWait()
            last_spoken_time = current_time  # Update the timestamp of the special message
        else:
            engine.say(message)
            engine.runAndWait()

        # Add a small delay to prevent CPU overload
        time.sleep(0.001)
    """
    while True:
        message = message_queue.get()
        engine.say(message)
        engine.runAndWait()
        _ = message_queue.get()
        # time.sleep(2)"""

# Start audio streaming
audio_thread = threading.Thread(target=text_to_speech, args=(message_queue,))
audio_thread.start()

# Load video
# cap = cv2.VideoCapture(r'C:\Users\birad\Documents\Embedded\video.mp4')  # Replace with your video path
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error opening video stream or file")

# fps_time = 0
sen = ""
while cap.isOpened():
    ret_val, image = cap.read()
    if not ret_val:
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resize_rgb = cv2.resize(image_rgb, (0, 0), None, .50, .50)
    results = pose.process(image_rgb)
    
    if results.pose_landmarks is not None:
        landmarks = results.pose_landmarks.landmark
        correct_angle_count = 0
        # for itr in [11,10,1,0,5,4,9,8,7,6,3,2]:
        for itr in [11, 10, 1, 0, 5, 4, 9, 8, 6, 3, 2, 7]:
            # Calculate angle
            point_a = (int(landmarks[angle_coordinates[itr][0]].x * image.shape[1]),
                        int(landmarks[angle_coordinates[itr][0]].y * image.shape[0]))
            point_b = (int(landmarks[angle_coordinates[itr][1]].x * image.shape[1]),
                        int(landmarks[angle_coordinates[itr][1]].y * image.shape[0]))
            point_c = (int(landmarks[angle_coordinates[itr][2]].x * image.shape[1]),
                        int(landmarks[angle_coordinates[itr][2]].y * image.shape[0]))

            angle_obtained = calculate_angle(point_a, point_b, point_c)
            # Check angle and update sen only if there is a significant change
            if angle_obtained < accurate_angle_lists[itr] - correction_value[itr]:
                status = "more"
                if itr == 7:
                   i = 7
                if itr == 10 or itr == 11:
                    i = 6
                if itr == 2 or itr == 3:
                    i = 5
                if itr == 0 or itr == 1:
                    i = 4
                # sen = "Straigthen your " + angle_descriptions[itr]
            elif angle_obtained > accurate_angle_lists[itr] + correction_value[itr]:
                status = "less"
                if itr == 7:
                   i = 7
                if itr == 10 or itr == 11:
                    i = 6
                if itr == 2 or itr == 3:
                    i = 5
                
                if itr == 0 or itr == 1:
                    i = 4
                
                # sen = "Bend your " + angle_descriptions[itr]
            else:
                status = "OK"
                correct_angle_count += 1

            
            # Display angle info on image
            (w, h), _ = cv2.getTextSize("Vrikshasana", cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
            cv2.rectangle(image, (10, image.shape[0] - 30), (10 + w, image.shape[0] - 10), (255, 255, 255), cv2.FILLED)
            cv2.putText(image, "Vrikshasana", (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

            status_position = (point_b[0] - int(image.shape[1] * 0.03), point_b[1] + int(image.shape[0] * 0.03))
            cv2.putText(image, f"{status}", status_position, cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

            cv2.putText(image, f"{angle_name_list[itr]}", (point_b[0] - 50, point_b[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
            
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
#             i = 0
        
        if i == 6:
            sen = "Straigthen your Spine"
        
        if i == 4:
            sen = "Join your hands properly"

        if i == 7:
            sen = "Raise your right leg a little higher"
        
        if i == 5:
            sen = "Raise your hands overhead"

        """if fps_time == 0:
            sen = "Lift your right leg and place it at the inner side of left thigh"
            # i = 2"""

        if correct_angle_count > 9:
            posture = "CORRECT"
            sen = "Perfecttttt, Hold for few breathe "
        else:
            posture = "WRONG"
        
        if message_queue.qsize() < 1:
                message_queue.put(sen)
        # posture = "CORRECT" if correct_angle_count > 9 else "WRONG"
        posture_color = (0, 255, 0) if posture == "CORRECT" else (0, 0, 255)
        posture_position = (10, 30)  # Điều chỉnh giá trị này để đặt văn bản
        cv2.putText(image, f"Yoga movements: {posture}", posture_position, cv2.FONT_HERSHEY_PLAIN, 1.5, posture_color, 2)               
        
#         fps_text = f"FPS: {1.0 / (time.time() - fps_time):.3f}"  # Hiển thị FPS với 3 chữ số sau dấu thập phân
#        fps_position = (10, 60)  # Điều chỉnh giá trị này để đặt văn bản
#        cv2.putText(image, fps_text, fps_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#        fps_time = time.time()

        cv2.imshow('Mediapipe Pose Estimation', image)
#        fps_time = time.time()

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()