import datetime
import sys

from googleapiclient.http import MediaFileUpload

from Google import Create_Service
from ismediafile import isMediaFile

CLIENT_SECRET_FILE = 'client_secret (2).json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

upload_date_time = datetime.datetime(2022, 2, 4, 22, 00, 0).isoformat() + '.000Z'

request_body = {
    'snippet': {
        'categoryI': 19,
        'title': 'Upload Testing',
        'description': 'Hello World Description',
        'tags': ['Travel', 'video test', 'Travel Tips']
    },
    'status': {
        'privacyStatus': 'private',
        # 'publishAt': upload_date_time,
        'selfDeclaredMadeForKids': False,
    },
    'notifySubscribers': False
}

if __name__ == '__main__':
    for item in sys.argv[1:]:
        mediaFile = MediaFileUpload(item)
        if isMediaFile(item):
            response_upload = service.videos().insert(
                part='snippet,status',
                body=request_body,
                media_body=mediaFile
            ).execute()

            service.thumbnails().set(
                videoId=response_upload.get('id'),
                media_body=MediaFileUpload('thumbnail.png')
            ).execute()
        else:
            print(f"This file is not a video: {item}")
