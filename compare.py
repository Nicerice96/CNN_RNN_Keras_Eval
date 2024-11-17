import os
import json

def create_folder_structure_json(path):
    result = {'name': os.path.basename(path), 'type': 'folder', 'children': []}
    if not os.path.isdir(path):
        return result
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            result['children'].append(create_folder_structure_json(entry_path))
        else:
            result['children'].append({'name': entry, 'type': 'file'})
    return result

def sorting(item):
    if isinstance(item, dict):
        return {key: sorting(value) for key, value in item.items()}
    if isinstance(item, list):
        return sorted((sorting(x) for x in item), key=lambda x: (x.get('name', ''), x.get('type', '')))
    else:
        return item

def compare_json_data(json1, json2):
    return sorting(json1) == sorting(json2)

def main():
    # Path to the folder and JSON file
    folder_path = 'Video'
    json_file_path = 'video_metadata.json'

    # Generate JSON representation of the folder structure
    folder_json = create_folder_structure_json(folder_path)

    # Load the existing JSON file
    with open(json_file_path, 'r') as json_file:
        existing_json = json.load(json_file)

    # Convert the existing JSON to a folder-like structure for comparison
    def convert_to_folder_structure(json_data):
        result = {'name': 'root', 'type': 'folder', 'children': []}
        for video_entry in json_data:
            folder_name = os.path.dirname(video_entry['video'])
            folder_entry = {'name': folder_name, 'type': 'folder', 'children': [{'name': os.path.basename(video_entry['video']), 'type': 'file'}]}
            result['children'].append(folder_entry)
        return result

    converted_json = convert_to_folder_structure(existing_json)

    # Compare the two JSON structures
    if compare_json_data(folder_json, converted_json):
        print("The folder structure and JSON file are identical.")
    else:
        print("The folder structure and JSON file are not identical.")

if __name__ == "__main__":
    main()