import os
import json

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

output_json = []

# Define a response for each category (video action)
action_descriptions = {
    "CPR": "This video shows Chest Compressions being performed on the baby.",
    "ETT": "This video shows endotracheal intubation insertion for airway management in the baby.",
    "PPV": "This video shows Postive Pressure Ventaliation being administered to the baby.",
    "Pulse Oximeter": "This video shows the use of a pulse oximetery to monitor the baby's oxygen levels.",
    "Suction": "This video shows suctioning being performed on the baby.",
    "Drying": "This video shows the drying procedure being performed on the baby.",
    "Reposition": "This video shows repositioning of the baby’s airway.",
    "UVC": "This video shows umbilical venous catheter insertion into the baby for intravenous access."
}

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
                description = action_descriptions.get(folder_name, "This video shows an action related to the specified category.")
                
                # Create the video entry with the new format
                video_entry = {
                    "video": os.path.join(folder_name, video),
                    "conversations": [
                        {
                            "from": "human",
                            "value": "Please provide a detailed description of the video."
                        },
                        {
                            "from": "gpt",
                            "value": description  # Use the specific description based on the category
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
