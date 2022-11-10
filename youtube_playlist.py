from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

#to write into csv file
def write_into_csv(items):
    with open('result.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(items)


options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service('/Users/tsere/Documents/selenium_webdrivers/chromedriver'), options=options)

url = input('Enter playlist URL: ').strip()
print("[*] Getting the information...")

driver.get(url)

SCROLL_PAUSE = 3
last_height = driver.execute_script('return document.documentElement.scrollHeight')
#to render all information on page
while True:
    driver.execute_script('window.scrollTo(0, arguments[0]);', last_height)
    time.sleep(SCROLL_PAUSE)
    new_height = driver.execute_script('return document.documentElement.scrollHeight')

    if new_height == last_height:
        break
    last_height = new_height

playlist_title = driver.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="text"]').text
playlist_content = driver.find_element(By.ID, 'contents')
channel_title = playlist_content.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="text"]').text
videos = playlist_content.find_elements(By.TAG_NAME, 'ytd-playlist-video-renderer')
number_of_videos = len(videos)

print(f'[+] Channel Title: {channel_title}')
print(f"[*] Getting the information from playlist: {playlist_title}")
print(f"[+] I have extracted {number_of_videos} video information and saved in result.csv file.")

for video in videos:
    title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id="video-title"]'))).text
    url = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id="video-title"]'))).get_attribute('href')
    thumbnail = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[id="img"]'))).get_attribute('src')
    write_into_csv([title, url, thumbnail])

driver.quit()

