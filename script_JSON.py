import os
import json

# Define the video folder and category mappings
video_folder = 'Videos'
folder_to_category = {
    "CPR": "Chest_Compression",
    "ETT": "ETT_Laryngeal",
    "PPV": "PPV",
    "Pulse Oximeter": "Pulse_Oximeter",
    "Suction": "Suction",
    "Drying": "Drying",
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
                
                # Get the action description for the category
                description = action_descriptions.get(folder_name, "This video shows an action related to neonatal resuscitation.")
                
                # Create the video entry with the specified format
                video_entry = {
                    "video": os.path.join(folder_name, video),  # Include folder path for correct reference
                    "conversations": [
                        {
                            "from": "human",
                            "value": "Please provide a detailed description of the video."
                        },
                        {
                            "from": "assistant",
                            "value": description
                        }
                    ]
                }
                output_json.append(video_entry)
    else:
        print(f"Folder does not exist: {folder_path}")

# Write the JSON output to a file
with open("video_metadata.json", "w") as outfile:
    json.dump(output_json, outfile, indent=4)

print("JSON file created successfully!")
