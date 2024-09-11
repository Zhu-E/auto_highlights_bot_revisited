# auto_highlights_bot_revisited

Requirements: 
 * A youtube API client secret file will need to be created.
 * The CLIENT_ID and CLIENT_SECRET in the twitchAPI.py file need to be updated to valid values associated with the twitch API.
 * All necessary libraries and dependencies must be installed. 

How it works:
1. The twitchAPI is used to generate a list of the top 20 clips given a game
2. A selenium webscraper is used to download the videos from the URLs associated with the clips
3. FFmpeg is used to combine the videos into a single .mp4 file
4. The YouTube API is used to automatically upload the video to YouTube

How to run:
Run the main.py file
