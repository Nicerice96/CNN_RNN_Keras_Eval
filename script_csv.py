import os
import pandas as pd 

video_folder = 'Videos'

folder_to_category = {
    "CPR": "Chest_Compression",
    "ETT": "ETT_Laryngeal",
    "PPV": "PPV",
    "Pulse Oximeter": "Pulse_Oximeter",
    "Suction" : "Suction",
    "Drying" : "Drying",
    "Reposition": "Position_Airway",
    "UVC": "UVC"
}

output_data = []

# Loop through each subfolder
for folder_name in folder_to_category:
    folder_path = os.path.join(video_folder, folder_name)
    
    print(f"Processing folder: {folder_path}")

    if os.path.isdir(folder_path):
        print(f"{folder_path} exists and is a directory.")
        
        for video in os.listdir(folder_path):  
            if video.endswith(".mp4"):  
                print(f"Found video: {video}")
                video_entry = {
                    "file_name": video,
                    "label": folder_to_category[folder_name],
                    "file_path": os.path.join(folder_path, video),   
                }
                output_data.append(video_entry)
    else:
        print(f"Folder does not exist: {folder_path}")

# Create a DataFrame and save it as a CSV file
df = pd.DataFrame(output_data)
df.to_csv("video_metadata.csv", index=False)

print("CSV file created successfully!")
