import os
import json
import random

# Define the video folder and category mappings
video_folder = 'Videos1'
folder_to_category = {
    "CPR": "Chest_Compression",
    "ETT": "ETT_Laryngeal",
    "PPV": "PPV",
    "Pulse Oximeter": "Pulse_Oximeter",
    "Suction": "Suction",
    "Drying-Warming-Stimulate": "Drying",  # Adjusted for the actual folder name
    "Reposition": "Position_Airway",
    "UVC": "UVC"
}

# Define action descriptions
action_descriptions = {
    "PPV": "This video shows a medical professional performing Positive Pressure Ventilation (PPV) on a newborn baby. They are using a bag-valve-mask device to provide assisted breathing support.",
    "CPR": "This video shows a healthcare provider performing chest compressions on a newborn baby. The compressions are being delivered at the appropriate depth and rate for neonatal resuscitation.",
    "ETT": "This video shows the process of endotracheal intubation being performed on a newborn baby. A medical professional is carefully inserting a breathing tube through the vocal cords.",
    "Drying": "This video shows medical staff thoroughly drying a newborn baby immediately after birth. This is an essential step to prevent heat loss and stimulate breathing.",
    "Pulse Oximeter": "This video shows the placement of a pulse oximeter on a newborn baby's right hand or wrist. This device is being used to monitor the baby's oxygen saturation and heart rate.",
    "Reposition": "This video shows healthcare providers repositioning a newborn baby's head and neck to establish an optimal airway position for breathing.",
    "Suction": "This video shows medical staff performing suction to clear amniotic fluid and secretions from a newborn baby's mouth and nose, ensuring clear airways.",
    "UVC": "This video shows the insertion of an umbilical venous catheter (UVC) into a newborn baby's umbilical cord. This provides immediate vascular access for medications or fluids if needed."
}

# Output list for the combined JSON file
all_videos_json = []

# Loop through each subfolder
for folder_name in folder_to_category:
    folder_path = os.path.join(video_folder, folder_name)
    print(f"Processing folder: {folder_path}")
    
    if os.path.isdir(folder_path):
        print(f"{folder_path} exists and is a directory.")
        
        # Collect all video files in the current folder
        video_files = [video for video in os.listdir(folder_path) if video.endswith(".mp4")]
        if not video_files:
            continue
        
        # Shuffle the video files to ensure randomness
        random.shuffle(video_files)
        
        # Helper function to create video entry
        def create_video_entry(video, folder):
            description = action_descriptions.get(folder_name, "This video shows an action related to neonatal resuscitation.")
            relative_video_path = os.path.join(folder, video)
            
            return {
                "video": relative_video_path,
                "conversations": [
                    {
                        "from": "human",
                        "value": "<video>Please provide a detailed description of the video."
                    },
                    {
                        "from": "gpt",
                        "value": description
                    }
                ]
            }
        
        # Add all video entries to the combined JSON
        for video in video_files:
            all_videos_json.append(create_video_entry(video, folder_name))
    
    else:
        print(f"Folder does not exist: {folder_path}")

# Write the JSON output to a single file
with open("all_videos.json", "w") as output_file:
    json.dump(all_videos_json, output_file, indent=4)

print("all_videos.json file created successfully!")
