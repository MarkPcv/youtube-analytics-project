import json
import os
import datetime
import isodate

import googleapiclient.discovery
from googleapiclient.discovery import build


class PlayList:
    # Define API key for YouTube account
    api_key = os.getenv('YT_API_KEY')
    # Create special object to work with API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        """
        Initialization of PlayList class instance
        """
        self.playlist = self.youtube.playlists().list(id=playlist_id,
                                                      part='contentDetails,'
                                                           'snippet',
                                                      maxResults=50,
                                                      ).execute()
        # Retrieve playlist title
        self.title = self.playlist['items'][0]['snippet']['title']
        # Retrieve video URL
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id
        # Keep playlist id
        self.__playlist_id = playlist_id

    def print_info(self):
        """Return dictionary in json-like comfortable format with indents"""
        print(json.dumps(self.playlist, indent=2, ensure_ascii=False))

    def __video_response(self) -> dict:
        """
        Returns a dictionary of each video information in playlist
        """
        # Get info about videos in playlist
        playlist_videos = self. \
            youtube.playlistItems().list(playlistId=self.__playlist_id,
                                         part='contentDetails',
                                         maxResults=50,
                                         ).execute()
        # Get ID of each video in playlist
        video_ids: list[str] = [video['contentDetails']['videoId']
                                for video in
                                playlist_videos['items']]
        # Get information of each video by its ID
        video_response = self.youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()

        return video_response

    @property
    def total_duration(self) -> datetime.timedelta:
        """
        Return duration of playlist
        """
        # Get duration of each video and sum it
        total = datetime.timedelta(seconds=0)
        for video in self.__video_response()['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self) -> str:
        """
        Returns the link to the video with most likes
        """
        most_liked = 0
        video_url = ''
        # Find most liked video in playlist
        for video in self.__video_response()['items']:
            num_likes = int(video['statistics']['likeCount'])
            if most_liked < num_likes:
                most_liked = num_likes
                video_url = "https://youtu.be/" + video['id']

        return video_url
    