import cv2

video_path = "CPR(3).mp4"  # Update with a problematic video path
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Couldn't open video.")
else:
    print("Video opened successfully.")
    cap.release()