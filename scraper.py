import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import twitchAPI
import re

def get_video_url(clip_url, driver):
    driver.get(clip_url)
    video_element = driver.find_element(By.XPATH, '//video[@playsinline]')
    return video_element.get_attribute('src')

def sanitize_filename(filename):
    # Remove or replace any characters that are not alphanumeric, spaces, or underscores
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)  # Remove invalid characters
    filename = filename.replace(" ", "_")  # Replace spaces with underscores
    return filename

def download_clip(clip, driver, download_folder):
    clip_url = clip['url']
    clip_name = clip['title']
    clip_name = sanitize_filename(clip_name)
    print('downloading ' + clip_url)
    video_url = get_video_url(clip_url, driver)
    if video_url:
        video_content = requests.get(video_url).content
        video_filename = os.path.join(download_folder, clip_name + '.mp4')  # Save in the specified folder
        with open(video_filename, 'wb') as video_file:
            video_file.write(video_content)

def download_clips(clips, driver, download_folder):
    os.makedirs(download_folder, exist_ok = True)
    for clip in clips:
        download_clip(clip, driver, download_folder)

def make_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_driver = webdriver.Chrome(options = chrome_options)
    return chrome_driver

if __name__ == '__main__':
    driver = make_driver()

    oauth_token = twitchAPI.get_oauth_token()
    game_id = twitchAPI.get_game_id(oauth_token, 'League of Legends')
    download_clips(twitchAPI.get_top_clips(game_id, oauth_token), driver, 'league_clips')

    driver.quit()




