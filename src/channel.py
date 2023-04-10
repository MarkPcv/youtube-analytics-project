import json
import os

import googleapiclient.discovery
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # Define API key for YouTube account
    api_key = os.getenv('YT_API_KEY')
    # Create special object to work with API
    youtube = build('youtube', 'v3', developerKey=api_key)

    @classmethod
    def get_service(cls):
        """Get object for YouTube API service"""
        return cls.youtube

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        """
        # Retrieve information about channel as JSON object
        self.channel = Channel.youtube.channels(). \
            list(id=channel_id, part='snippet,statistics').execute()
        # Retrieve channel id
        self.__channel_id = channel_id
        # Retrieve channel title
        self.title = self. \
            channel['items'][0]['snippet']['title']
        # Retrieve channel description
        self.description = self. \
            channel['items'][0]['snippet']['description']
        # Retrieve channel URL
        self.url = "https://www.youtube.com/channel/" + channel_id
        # Retrieve number of subscribers
        self.subs_count = self. \
            channel['items'][0]['statistics']['subscriberCount']
        # Retrieve total number of videos
        self.video_count = self. \
            channel['items'][0]['statistics']['videoCount']
        # Retrieve total number of videos
        self.view_count = self. \
            channel['items'][0]['statistics']['viewCount']


    def __str__(self):
        """
        Provides a string representation of class object for user such as:
        channel
        """
        return f"{self.title} ({self.url})"


    def print_info(self) -> None:
        """Return dictionary in json-like comfortable format with indents"""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        """
        Getter for attribute "channel_id"
        """
        return self.__channel_id

    def to_json(self, filename):
        """
        Record class attributes into JSON file
        """
        with open(filename, 'w') as file:
            dict_ = {
                'channel_id': self.channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subs_count': self.subs_count,
                'video_count': self.video_count,
                'view_count': self.view_count
            }
            json.dump(dict_, file, ensure_ascii=False)
