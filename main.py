import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    creds = None

    # Load token if exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)

    # If no login yet → open browser
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

        # Save login session
        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)

    service = build('drive', 'v3', credentials=creds)

    # FILE TO UPLOAD
    file_path = 'test.sql'

    file_metadata = {
        'name': 'backup.sql'
    }

    media = MediaFileUpload(file_path)

    service.files().create(
        body=file_metadata,
        media_body=media
    ).execute()

    print("Upload successful!")

if __name__ == '__main__':
    main()