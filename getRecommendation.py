from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import requests
import sys
import pprint
import os
import random
import json

#Gets recommendation names and artists from seed genres
'''
HAVE TO LOG OUT OF SPOTIFY ON COMPUTER BEFORE RUNNING
AND WHEN PROMTED TO LOG IN USE:
email = 'RecommendationSpotify@gmail.com'
pass = 'RecommendationSpotify'
'''


def from_book_playlist(book_name, book_genres, token):

    playlists = []
    songs = []

    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }

    for genre in book_genres:
        URL = "https://api.spotify.com/v1/search?q={query}&type=playlist&limit=1".format(query = genre)
        r = requests.get(url = URL, headers = HEADERS)
        playlists.append(r.json()['playlists']['items'][0]['external_urls']['spotify'].split('/')[-1])

    URL = "https://api.spotify.com/v1/search?q={query}&type=playlist&limit=5".format(query = book_name)
    r = requests.get(url = URL, headers = HEADERS)
    for i in range(5):
        playlists.append(r.json()['playlists']['items'][i]['external_urls']['spotify'].split('/')[-1])


    for playlist in playlists:
        URL = "https://api.spotify.com/v1/playlists/{id}/tracks".format(id = playlist)
        r = requests.get(url = URL, headers = HEADERS)
        json = r.json()
        if json['items']:
            songs.append(json['items'][random.randint(0, min(100,r.json()['total']) - 1)]['track']['uri'])

    return songs


def recommend(book_name, genres, nSongs):

    # Log into spotify
    client_id='445eea96fba74cf285bd484b0309b2f5'
    client_secret='a20b5364f19f4fc5ab51edd1fcfe2d8c'

    username = '31moc3d6qqfzva4zwket2g6zsuae'
    # password = 'RecommendationSpotify'
    # email = 'RecommendationSpotify@gmail.com'
    # email pass = 'RecommendationSpotify1!'

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

    try:
        os.remove(f".cache-{username}")
    except:
        pass

    TOKEN = spotipy.util.prompt_for_user_token(
    scope='playlist-modify-public', 
    username=username,
    client_id=client_id, 
    client_secret=client_secret, 
    redirect_uri="http://localhost:8888/callback")


    from spotipy.oauth2 import SpotifyOAuth

    # Creates playlist to add songs to
    sp = spotipy.Spotify(TOKEN)
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, name=f"{book_name} recommendations", public=True)

    try:
        os.remove(f".cache-{username}")
    except:
        pass

    result = sp.recommendations(seed_genres=genres, limit=nSongs)
    urls = []
    uris = []

    uris += from_book_playlist(book_name, genres, TOKEN)
    
    for i in result['tracks']:
        urls.append(i['external_urls']['spotify'])
        uris.append(i['uri'])

    

    # Adds songs to playlist
    # print(urls)
    sp.user_playlist_add_tracks(user_id, playlist["id"], uris)
    return playlist['id']