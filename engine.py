import combiner
import scraper
import twitchAPI
import youtubeAPI
import shutil
import os
import pandas as pd
import ast

def delete_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"{directory_path} and its contents have been deleted.")
    else:
        print(f"{directory_path} does not exist.")

def cleanup():
    delete_directory('clips')
    delete_directory('output_directory')

def upload_video(creds, game_name, num_clips, timeframe, description, tags, title, episode):
    # Cleanup previous runs
    cleanup()

    # Find the top clips
    top_clips = twitchAPI.get_clips_given_game_name(game_name, num_clips, timeframe)

    # Download the top clips
    driver = scraper.make_driver()
    scraper.download_clips(top_clips, driver, 'clips')
    driver.close()

    # Combine clips into one video
    combiner.combine_mp4_files_from_directory('clips', 'output_directory', output_filename='output.mp4')

    video_file = "output_directory/output.mp4"  # Path to the video file

    youtubeAPI.upload_video(creds, video_file, title+str(episode), description, tags=ast.literal_eval(tags), privacy_status="public")

def parse_params_csv(path):
    df = pd.read_csv('params.csv', usecols = ['cred_path', 'game_name', 'num_clips', 'timeframe', 'description', 'tags', 'title', 'episode'])
    for row in df.itertuples():
        creds = youtubeAPI.creds_from_file(row.cred_path)
        upload_video(creds, row.game_name, row.num_clips, row.timeframe, row.description, row.tags, row.title, row.episode)
    df['episode'] = df['episode'] + 1
    df.to_csv('params.csv')