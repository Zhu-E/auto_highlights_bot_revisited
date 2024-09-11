import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# Define your YouTube scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(video_file, title, description, category="22", tags=None, privacy_status="private"):
    # Set up OAuth 2.0 flow
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "youtube_client_secret.json", SCOPES)
    credentials = flow.run_local_server(port=8080)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    # Define the request metadata
    request_body = {
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

    # Upload the video file
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()

    print(f"Video uploaded successfully. Video ID: {response['id']}")

if __name__ == "__main__":
    # Replace with your video details
    video_file = "output_directory/combined_video.mp4"  # Path to the video file
    title = "test vid"
    description = "This is a test upload via the YouTube API."
    tags = ["sample", "API", "YouTube"]

    upload_video(video_file, title, description, tags=tags, privacy_status="public")