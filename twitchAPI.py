import requests
from datetime import datetime, timedelta, timezone
import json

# These need to be filled in with the CLIENT_ID and CLIENT_SECRET
# associated with the Twitch API in order for the code to run.
# Note that this client_secret is no longer valid as a new client_secret was
# generated after uploading to github for privacy reasons.
# Function to load client_id and client_secret from the JSON file
def load_credentials():
    with open('twitch_credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials['CLIENT_ID'], credentials['CLIENT_SECRET']

# Load the client_id and client_secret from the JSON file
CLIENT_ID, CLIENT_SECRET = load_credentials()


# Get OAuth token
def get_oauth_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params = params)
    response.raise_for_status()
    return response.json()['access_token']


# Get game ID given the name of a game
def get_game_id(oauth_token, name):
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {oauth_token}'
    }
    url = 'https://api.twitch.tv/helix/games'
    params = {
        'name': name
    }
    response = requests.get(url, headers = headers, params = params)
    response.raise_for_status()
    return response.json()['data'][0]['id']

def set_params(id_type, category_id, num_clips, timeframe):
    started_at = (datetime.now(timezone.utc) - timedelta(days = timeframe)).strftime(
        '%Y-%m-%dT%H:%M:%SZ')
    if id_type == 'game':
        params = {
            'game_id': category_id,
            'first': num_clips,  # Number of clips to retrieve
            'started_at': started_at,
        }
    elif id_type == 'broadcaster':
        params = {
            'broadcaster_id': category_id,
            'first': num_clips,  # Number of clips to retrieve
            'started_at': started_at,
        }
    else:
        raise Exception('invalid id_type')
    return params

# Get top clips given a game id
def get_top_clips(oauth_token, category_id, num_clips, id_type, timeframe):
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {oauth_token}'
    }
    url = 'https://api.twitch.tv/helix/clips'
    params = set_params(id_type, category_id, num_clips, timeframe)
    # Calculate the current UTC time and subtract 24 hours

    response = requests.get(url, headers = headers, params = params)
    response.raise_for_status()
    return response.json()['data']

def get_clips_given_game_name(game_name, num_clips, timeframe):
    twitch_oauth = get_oauth_token()
    game_id = get_game_id(twitch_oauth, game_name)
    top_clips = get_top_clips(twitch_oauth, game_id, num_clips, 'game', timeframe)
    return top_clips

def get_clips_given_broadcaster_name(game_name, num_clips, timeframe):
    twitch_oauth = get_oauth_token()
    game_id = get_game_id(twitch_oauth, game_name)
    top_clips = get_top_clips(twitch_oauth, game_id, num_clips, 'broadcaster', timeframe)
    return top_clips

# Main function
def main():
    # Get OAuth token
    oauth_token = get_oauth_token()

    # Get game ID for chosen game
    game_id = get_game_id(oauth_token, 'League of Legends')

    clips = get_top_clips(oauth_token, game_id, 20, 'game', 1)

    # Display Clips
    for clip in clips:
        print(clip)


if __name__ == '__main__':
    main()
