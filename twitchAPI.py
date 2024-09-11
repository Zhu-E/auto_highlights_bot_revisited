import requests
from datetime import datetime, timedelta

# These need to be filled in with the CLIENT_ID and CLIENT_SECRET
# associated with the Twitch API in order for the code to run.
# Note that this client_secret is no longer valid as a new client_secret was
# generated after uploading to github for privacy reasons.
CLIENT_ID = 'vx8smd2dxpzw061tbvzjbyr2vvje0l'
CLIENT_SECRET = 'k2zljfgz9y26svv8cahltmc509tet4'


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


# Get top clips given a game id
def get_top_clips(oauth_token, game_id):
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {oauth_token}'
    }

    # Calculate the current UTC time and subtract 24 hours
    started_at = (datetime.utcnow() - timedelta(days = 1)).strftime('%Y-%m-%dT%H:%M:%SZ')

    url = 'https://api.twitch.tv/helix/clips'
    params = {
        'game_id': game_id,
        'first': 20,  # Number of clips to retrieve
        'started_at': started_at,
    }
    response = requests.get(url, headers = headers, params = params)
    response.raise_for_status()
    return response.json()['data']

def returned_clips(game_name):
    twitch_oauth = get_oauth_token()
    game_id = get_game_id(twitch_oauth, game_name)
    top_clips = get_top_clips(twitch_oauth, game_id)
    return top_clips

# Main function
def main():
    # Get OAuth token
    oauth_token = get_oauth_token()

    # Get game ID for chosen game
    game_id = get_game_id(oauth_token, 'League of Legends')

    clips = get_top_clips(oauth_token, game_id)

    # Display Clips
    for clip in clips:
        print(clip)


if __name__ == '__main__':
    main()
