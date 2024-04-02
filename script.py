import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from os import getenv, path
import json


# saves tag data to file
def save_data(tag_data, filename='tag_data.json'):
    with open(filename, 'w') as file:
        json.dump(tag_data, file)

# loads it back from file
def load_data(filename='tag_data.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        print("Opened file, returning JSON.")
        return {int(k): v for k, v in data.items()}
    except FileNotFoundError:
        print("File not found. Starting with an empty dictionary.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}.")
        return {}
    except ValueError:
        print("Error converting keys to integers.")
        return {}


# a spotify client object to use the spotify API
def sp_client():

    # authentication parameters!
    SPOTIFYSCOPE = "playlist-modify-private playlist-read-private playlist-modify-public playlist-read-collaborative user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-modify user-library-read user-read-playback-position user-read-recently-played user-top-read app-remote-control streaming user-follow-modify user-follow-read"
    SPOTIPY_CLIENT_ID = getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REFRESH_TOKEN = getenv("SPOTIPY_REFRESH_TOKEN")

    # authorisation with OAuth2
    auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                client_secret=SPOTIPY_CLIENT_SECRET,
                                redirect_uri="https://avishspf.com/",
                                scope=SPOTIFYSCOPE)

    # creates and returns a client object using the provided token
    token_info = auth_manager.refresh_access_token(SPOTIPY_REFRESH_TOKEN)
    return spotipy.Spotify(token_info["access_token"])
    

# creates a spotify client and gets my primary device ID
sp = sp_client()
SPOTIFY_DEVICE_ID = sp.devices()["devices"][0]["id"]


# starts spotify playback based on a provided tag with an API call
def start_spotify_playback(tag_id: int, spotify_client=sp, device=SPOTIFY_DEVICE_ID) -> None:
    spotify_client.start_playback(device_id=device, context_uri=tag_data[tag_id])


# does the inverse: gets the context URI based on the user's current listening activity
def get_current_playing_context_uri(spotify_client=sp):

    try:
        # gets the current playback and tries to return the URI and link back to Spotify
        current_playback = spotify_client.current_playback()
        if current_playback is not None and 'context' in current_playback and current_playback['context'] is not None:
            return current_playback['context']['uri'], current_playback['context']['external_urls']['spotify']
        return None, None

    except spotipy.SpotifyException as e:
        return None, None


# stores the mapping of tag data to Spotify URIs
tag_data: dict[int, str] = load_data()

# when a tag is presented
def on_tag_read(tag_id: int):
    global tag_data

    # if it has been registered already, play the corresponding context
    if tag_id in tag_data:
        print("Found registered tag ID - starting playback!")
        start_spotify_playback(tag_id)

    # otherwise, attempt to register the tag
    else:
        print("New tag ID detected - attempting to register.")
        context_uri, spotify_url = get_current_playing_context_uri()

        # if the function fails, just ignore
        if context_uri is None:
            print("Could not determine currently playing album/playlist.")
        
        # otherwise, we can register the tag as the current playback context for later
        else:
            print(f"Registered tag as [{context_uri}] (plays {spotify_url}).")
            tag_data[tag_id] = context_uri

    # wait to avoid repeatedly playing
    sleep(2)

# reader object from the RFID reader library
reader = SimpleMFRC522()

print("Present the tag to read.")
while not path.exists("/home/pi/cassette-project/shutdown_indicator"):
    print("Awaiting tag.")
    tag_id, text = reader.read_no_block()

    # If we have a tag, then trigger the function
    if tag_id is not None:
        on_tag_read(tag_id)

# saves the tags to a file, and cleans up GPIO pins
print("Saving data and exiting program.")
save_data(tag_data)
GPIO.cleanup()
