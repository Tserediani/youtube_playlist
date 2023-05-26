from enum import Enum, auto


from models.models import Youtube
from data.data_utils import correct_file_extension
from common.constants import BASE_URL, FILENAME, FORMAT
import chromedriver_binary
from web_scraping.web_scraping_utils import fetch_html, get_playlist_info, get_videos

import pandas as pd
import os


class OutputFormat(Enum):
    CSV = auto()
    XLSX = auto()


def write_data(
    data: Youtube,
    format: OutputFormat = OutputFormat.CSV,
) -> None:
    """Function to write data into file.\n
    Default format is CSV."""

    data = {
        "channel_name": data.playlist_info.channel_name,
        "playlist_title": data.playlist_info.playlist_title,
        "number_of_videos": data.playlist_info.number_of_videos,
        "title": data.video_info.title,
        "url": data.video_info.url,
        "thumbnail": data.video_info.thumbnail,
    }

    dataframe = pd.DataFrame([data])
    if format == OutputFormat.CSV:
        filename = correct_file_extension(FILENAME, ".csv")
        dataframe.to_csv(
            filename,
            header=not os.path.exists(filename),
            index=False,
            mode="a",
            sep="|",
        )
    elif format == OutputFormat.XLSX:
        filename = correct_file_extension(FILENAME, ".xlsx")
        # If the file doesn't exists just create new file and write data
        if not os.path.exists(filename):
            dataframe.to_excel(filename, index=False)
        # otherwise read existing data concatenate it into new dataframe and write into same file.
        old_dataframe = pd.read_excel(filename)
        new_dataframe = pd.concat([dataframe, old_dataframe])
        new_dataframe.to_excel(
            filename,
            index=False,
        )


def main():
    html_data = fetch_html(BASE_URL)

    playlist_info = get_playlist_info(html_data)
    for video in get_videos(html_data):
        write_data(
            Youtube(playlist_info=playlist_info, video_info=video),
            format=OutputFormat.XLSX if FORMAT.lower() == "xlsx" else OutputFormat.CSV,
        )


if __name__ == "__main__":
    main()
