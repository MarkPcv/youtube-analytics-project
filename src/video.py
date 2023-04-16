import json
import os

import googleapiclient.discovery
from googleapiclient.discovery import build


class Video:
    # Define API key for YouTube account
    api_key = os.getenv('YT_API_KEY')
    # Create special object to work with API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """
        Initialization of Video class instance
        """
        self.video_id = video_id
        self.video = Video.youtube.videos().list(part='snippet,statistics,'
                                                'contentDetails,topicDetails',
                                           id=video_id).execute()
        # Retrieve video title
        self.title = self. \
            video['items'][0]['snippet']['title']
        # Retrieve video URL
        self.url = "https://www.youtube.com/watch?v=" + video_id
        # Retrieve number of views
        self.view_count = self. \
            video['items'][0]['statistics']['viewCount']
        # Retrieve number of likes
        self.like_count = self. \
            video['items'][0]['statistics']['likeCount']

    def print_info(self):
        """Return dictionary in json-like comfortable format with indents"""
        print(json.dumps(self.video, indent=2, ensure_ascii=False))
