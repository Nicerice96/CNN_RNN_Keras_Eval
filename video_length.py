import os
from moviepy import VideoFileClip

# Define the root folder (you can replace this with the actual path)
root_folder = "Videos1"

# Initialize a list to store video paths that are above 30 seconds
long_videos = []

# Loop through the folders
for folder_name in os.listdir(root_folder):
    folder_path = os.path.join(root_folder, folder_name)
    if os.path.isdir(folder_path):
        # Loop through the files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                try:
                    # Get the duration of the video file
                    video = VideoFileClip(file_path)
                    video_duration = video.duration  # Duration in seconds
                    if video_duration > 30:
                        long_videos.append(file_path)
                    video.close()  # Always close the video to free resources
                except Exception as e:
                    print(f"Could not process video {file_path}: {e}")

# Print the paths of videos longer than 30 seconds
if long_videos:
    print("Videos longer than 30 seconds:")
    for video in long_videos:
        print(video)
else:
    print("No videos longer than 30 seconds were found.")
