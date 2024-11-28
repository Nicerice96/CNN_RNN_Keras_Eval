import os
import json
import random

# Define the video folder and category mappings
video_folder = 'Videos2'
folder_to_category = {
    "CPR": "Chest Compression",
    "ETT": "Endotracheal Intubation",
    "PPV": "Positive Pressure Ventilation",
    "Pulse Oximeter": "Pulse Oximetry",
    "Suction": "Suction",
    "Drying-Warming-Stimulate": "Drying",
    "Reposition": "Reposition",
    "UVC": "Umbilical Venous Catheter"
}

# Define action descriptions
action_descriptions = {
    "Positive Pressure Ventilation": "1",
    "Chest Compression": "2",
    "Endotracheal Intubation": "3",
    "Drying": "4",
    "Pulse Oximetry": "5",
    "Reposition": "6",
    "Suction": "7",
    "Umbilical Venous Catheter": "8"
}

# Output lists for train and eval JSON files
train_output = []
eval_output = []

# Loop through each subfolder
for folder_name, category in folder_to_category.items():
    folder_path = os.path.join(video_folder, folder_name)
    print(f"Processing folder: {folder_path}")

    if os.path.isdir(folder_path):
        # Collect all video files in the current folder
        video_files = [video for video in os.listdir(folder_path) if video.endswith(".mp4")]
        if not video_files:
            print(f"No video files found in folder: {folder_path}")
            continue

        # Shuffle the video files to ensure randomness
        random.shuffle(video_files)

        # Determine split point for 80/20 split
        split_index = int(0.8 * len(video_files))

        # Split videos into training and evaluation sets
        train_videos = video_files[:split_index]
        eval_videos = video_files[split_index:]

        # Helper function to create video entry
        def create_video_entry(video, folder, category):
            description = action_descriptions.get(category, "This video shows an action related to neonatal resuscitation.")
            relative_video_path = os.path.join(folder, video)

            return {
                "video": relative_video_path,
                "conversations": [
                    {
                        "from": "human",
                        "value": "ACTION CLASSIFICATION TASK\nClassify this neonatal resuscitation action video with the corresponding action number:\n1=Positive Pressure Ventilation\n2=Chest Compression\n3=Endotracheal Intubation\n4=Drying\n5=Pulse Oximetry\n6=Reposition\n7=Suction\n8=Umbilical Venous Catheter"
                    },
                    {
                        "from": "gpt",
                        "value": description
                    }
                ]
            }

        # Create train entries
        for video in train_videos:
            train_output.append(create_video_entry(video, folder_name, category))

        # Create eval entries
        for video in eval_videos:
            eval_output.append(create_video_entry(video, folder_name, category))

    else:
        print(f"Folder does not exist: {folder_path}")

# Write the JSON output to train.json and eval.json files
train_json_path = "train.json"
eval_json_path = "eval.json"

with open(train_json_path, "w") as train_file:
    json.dump(train_output, train_file, indent=4)

with open(eval_json_path, "w") as eval_file:
    json.dump(eval_output, eval_file, indent=4)

print(f"Train JSON file created: {train_json_path}")
print(f"Eval JSON file created: {eval_json_path}")