from pydantic import BaseModel, validator
from typing import Optional

from data.data_utils import clean_text

class Playlist(BaseModel):
    channel_name: str
    playlist_title: str
    number_of_videos: int

class Video(BaseModel):
    title:str
    url: str
    thumbnail: Optional[str]

    @validator('title')
    def title_cleaning(cls, title):
        return clean_text(title)


class Youtube(BaseModel):
    playlist_info: Playlist
    video_info: Video