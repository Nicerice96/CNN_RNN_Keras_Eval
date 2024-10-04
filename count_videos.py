import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
# Video Folder ID: Replace with your actual Videos folder ID
videos_folder_id = '1pVjVtEvlH1tg_3g8d3efOUbKAmiPGfKP'

def authenticate_google_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

def count_files_in_videos_folder(service, total):
    # List all subfolders in the specified Videos folder
    query = f"'{videos_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
    subfolders = service.files().list(q=query, fields="files(id, name)").execute().get('files', [])

    # Dictionary to hold the count of files in each subfolder
    file_counts = {}

    for subfolder in subfolders:
        subfolder_name = subfolder['name']
        subfolder_id = subfolder['id']
        
        # List all video files in the current subfolder
        query = f"'{subfolder_id}' in parents and mimeType='video/mp4'"
        videos = service.files().list(q=query, fields="files(id, name)").execute().get('files', [])
        
        # Count the number of videos in the folder
        file_count = len(videos)
        file_counts[subfolder_name] = file_count
        print(f"Folder '{subfolder_name}' contains {file_count} video files.")
        total += file_count
        

    return total

if __name__ == '__main__':
    # Authenticate and initialize the Google Drive API
    service = authenticate_google_drive()
    total = 0
    # Count the files in the Videos folder
    total += count_files_in_videos_folder(service, total)
    
    print(f"Total Videos: {total} ")
