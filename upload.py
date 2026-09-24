import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)

    service = build('drive', 'v3', credentials=creds)

    file_path = 'test.sql'

    file_metadata = {
        'name': f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql",
        'parents': ['1hCGvOS6J5yvLpIdVo9RobWIO-jXZQLDi']
    }

    media = MediaFileUpload(file_path)

    service.files().create(
        body=file_metadata,
        media_body=media
    ).execute()

    print("Upload successful!")

if __name__ == '__main__':
    main()