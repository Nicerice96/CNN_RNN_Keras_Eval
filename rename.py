import os
import datetime

# Define the video folder
video_folder = 'Videos'

# Loop through each subfolder
for folder_name in os.listdir(video_folder):
    folder_path = os.path.join(video_folder, folder_name)
    if os.path.isdir(folder_path):
        print(f"Processing folder: {folder_path}")
        for video in os.listdir(folder_path):
            if video.endswith(".mp4"):
                # Generate a base new file name
                base_video_name = f"{datetime.date.today().strftime('%Y%m%d')}_{folder_name}_{video}"
                base_video_name = base_video_name.replace(' ', '_').replace('(', '_').replace(')', '_')
                
                # Generate the new file name and ensure uniqueness
                new_video_name = base_video_name
                new_video_path = os.path.join(folder_path, new_video_name)
                old_video_path = os.path.join(folder_path, video)

                # Check for existing files with the same name
                counter = 1
                while os.path.exists(new_video_path):
                    # If there's a name conflict, append a counter to the file name
                    name, extension = os.path.splitext(base_video_name)
                    new_video_name = f"{name}_{counter}{extension}"
                    new_video_path = os.path.join(folder_path, new_video_name)
                    counter += 1

                # Rename the file
                os.rename(old_video_path, new_video_path)
                print(f"Renamed {video} to {new_video_name}")
