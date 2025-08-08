from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_authenticated_service():
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    credentials = flow.run_local_server(port=8080)
    return build("youtube", "v3", credentials=credentials)

def fetch_comments(video_id, max_results=100):
    youtube = get_authenticated_service()
    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100
    )

    response = request.execute()

    while response:
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        if "nextPageToken" in response and len(comments) < max_results:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=response["nextPageToken"]
            )
            response = request.execute()
        else:
            break

    return comments
