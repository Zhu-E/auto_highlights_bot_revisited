import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import json

# Define your YouTube scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def make_response_body(category, title, description, tags, privacy_status):
    return {
        "snippet": {
            "categoryId": category,
            "title": title,
            "description": description,
            "tags": tags or []
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

def download_creds(path):
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "youtube_client_secret.json", SCOPES)
    credentials = flow.run_local_server(port = 8080)
    creds_json = credentials.to_json()
    with open(path, 'w') as token_file:
        token_file.write(creds_json)
    return credentials


def creds_from_file(path):
    # Read the credentials JSON from the file
    with open(path, 'r') as token_file:
        creds_data = json.load(token_file)

    # Rebuild the credentials object from the saved JSON
    credentials = Credentials.from_authorized_user_info(creds_data, SCOPES)
    return credentials

def build_youtube_api(creds):
    youtube_API = googleapiclient.discovery.build("youtube", "v3", credentials = creds)
    return youtube_API



def upload_video(credentials, video_file, title, description, category="22", tags=None, privacy_status="private"):
    # Set up OAuth 2.0 flow
    youtube_API = build_youtube_api(credentials)

    # Define the request metadata
    request_body = make_response_body(category, title, description, tags, privacy_status)

    # Upload the video file
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube_API.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    response = request.execute()
    print(f"Video uploaded successfully. Video ID: {response['id']}")

if __name__ == "__main__":
    # Replace with your video details
    video_file_path = "output_directory/combined_video.mp4"  # Path to the video file
    video_title = "test vid"
    video_description = "This is a test upload via the YouTube API."
    video_tags = ["sample", "API", "YouTube"]

    upload_video(video_file_path, video_title, video_description, tags=video_tags, privacy_status="public")