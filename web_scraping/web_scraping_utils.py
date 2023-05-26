from urllib.parse import urljoin
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from common.constants import SCROLL_PAUSE, BASE_DOMAIN, WORKING_DIR
from models.models import Playlist, Video

import time


def create_browser() -> Chrome:
    options = Options()
    options.add_argument("--headless")
    # TO DISABLE LOGGING
    options.add_argument("--log-level=3")
    # TO DISABLE LOGGING FOR CHROMIUM
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = Chrome(options=options)

    return driver


def scroll(driver: Chrome) -> None:
    """Function that scrolls all the way bottom"""
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    # to render all information on page
    while True:
        driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
        time.sleep(SCROLL_PAUSE)
        new_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )

        if new_height == last_height:
            break
        last_height = new_height


def fetch_html(url) -> BeautifulSoup:
    """Creates Selenium Chrome Object,
    loads dynamic elements and returns BeautifulSoup Object"""
    driver = create_browser()
    driver.get(url)
    scroll(driver)

    return BeautifulSoup(driver.page_source, "lxml")


def get_playlist_info(html_data: BeautifulSoup) -> Playlist:
    """This function Parses given html and extracts Playlist information"""
    playlist_title = html_data.select_one('yt-formatted-string[id="text"]').get_text()
    channel_title = html_data.select_one(
        'yt-formatted-string[id="owner-text"]'
    ).get_text()
    number_of_videos = len(
        html_data.select('div[id="contents"] ytd-playlist-video-renderer')
    )

    return Playlist(
        channel_name=channel_title,
        playlist_title=playlist_title,
        number_of_videos=number_of_videos,
    )


def get_videos(html_data: BeautifulSoup) -> Video:
    """This function Parses given html and extracts Video details"""
    for video in html_data.select('div[id="contents"] ytd-playlist-video-renderer'):
        title = video.select_one('a[id="video-title"]').get_text()
        url = video.select_one('a[id="video-title"]').get("href")
        thumbnail = video.select_one('a[id="thumbnail"] img').get("src")

        yield Video(title=title, url=urljoin(BASE_DOMAIN, url), thumbnail=thumbnail)
