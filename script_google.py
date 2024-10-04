import os 
import pickle
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
video_folder_id = '1pVjVtEvlH1tg_3g8d3efOUbKAmiPGfKP'
folder_to_category = {
    "CPR": "Chest_Compression",
    "ETT": "ETT_Laryngeal",
    "Suction" : "Suction",
    "PPV": "PPV",
    "Pulse Oximeter": "Pulse_Oximeter",
    "Reposition": "Position_Airway",
    "UVC": "UVC",
    "Drying" : "Drying"
}


output_data = []
def authenticate_google_drive():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

def convert_video_folder_to_csv(service):
    # List all subfolders in the specified folder
    query = f"'{video_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
    subfolders = service.files().list(q=query, fields="files(id, name)").execute().get('files', [])

    for folder in subfolders:
        folder_name = folder['name']
        print(f"Processing folder: {folder_name}")

        if folder_name in folder_to_category:
            # List videos in the current subfolder
            query = f"'{folder['id']}' in parents and mimeType='video/mp4'"
            videos = service.files().list(q=query, fields="files(id, name)").execute().get('files', [])

            for video in videos:
                print(f"Found video: {video['name']}")
                video_entry = {
                    "file_name": video['name'],
                    "label": folder_to_category[folder_name],
                    "file_path": f"https://drive.google.com/uc?id={video['id']}",  # Direct link to the file
                }
                output_data.append(video_entry)
        else:
            print(f"No category mapping for folder: {folder_name}")

    # Create a DataFrame and save it as a CSV file
    df = pd.DataFrame(output_data)
    df.to_csv("video_metadata.csv", index=False)
    print("CSV file created successfully!")

if __name__ == '__main__':
    # Authenticate and initialize the Google Drive API
    service = authenticate_google_drive()
    
    # Convert video folder to CSV
    convert_video_folder_to_csv(service)

