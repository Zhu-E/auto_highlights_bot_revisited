import combiner
import scraper
import twitchAPI
import youtubeAPI
import shutil
import os

def delete_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"{directory_path} and its contents have been deleted.")
    else:
        print(f"{directory_path} does not exist.")

def main():
    # Cleanup from previous program runs
    delete_directory('league_clips')
    delete_directory('output_directory')

    # Find the top clips
    top_clips = twitchAPI.returned_clips('League of Legends')

    # Download the top clips
    driver = scraper.make_driver()
    scraper.download_clips(top_clips, driver, 'league_clips')

    # Combine clips into one video
    combiner.combine_mp4_files_from_directory('league_clips', 'output_directory', output_filename='output.mp4')

    video_file = "output_directory/output.mp4"  # Path to the video file
    title = "test vid" # Title of video
    description = "This is a test upload via the YouTube API." # Video description
    tags = ["sample", "API", "YouTube"] # Video Tags
    youtubeAPI.upload_video(video_file, title, description, tags=tags, privacy_status="public")


if __name__ == "__main__":
    main()