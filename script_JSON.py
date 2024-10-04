import os
import json


video_folder = 'Videos'  


folder_to_category = {
    "CPR": "Chest_Compression",
    "ETT": "ETT_Laryngeal",
    "PPV": "PPV",
    "Pulse Oximeter": "Pulse_Oximeter",
    "Reposition": "Position_Airway",
    "UVC": "UVC"
}

output_json = []

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
                    "category": folder_to_category[folder_name],
                    "file_path": os.path.join(folder_path, video),  
                    "duration": "Unknown",  
                    "annotations": "Description here"  
                }
                output_json.append(video_entry)
    else:
        print(f"Folder does not exist: {folder_path}")

with open("video_metadata.json", "w") as outfile:
    json.dump(output_json, outfile, indent=4)

print("JSON file created successfully!")
