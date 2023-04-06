import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # Define API key for YouTube account
    api_key = os.getenv('YT_API_KEY')
    # Create special object to work with API
    youtube = build('youtube', 'v3', developerKey=api_key)

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
        self.title = self.channel['items'][0]['snippet']['title']
        # Retrieve channel description
        self.description = self.channel['items'][0]['snippet']['description']
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

    def print_info(self) -> None:
        """Return dictionary in json-like comfortable format with indents"""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id
