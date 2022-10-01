from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint
import os

#Gets recommendation names and artists from seed genres
'''
HAVE TO LOG OUT OF SPOTIFY ON COMPUTER BEFORE RUNNING
AND WHEN PROMTED TO LOG IN USE:
email = 'RecommendationSpotify@gmail.com'
pass = 'RecommendationSpotify'
'''

book_name = input("Enter a book name: ")
genres = input("Enter some music genres: ")
nSongs = input("Enter the number of songs you want: ")

genres = genres.split(' ')

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

token = spotipy.util.prompt_for_user_token(
scope='playlist-modify-public', 
username=username,
client_id=client_id, 
client_secret=client_secret, 
redirect_uri="http://localhost:8888/callback")


from spotipy.oauth2 import SpotifyOAuth

# Creates playlist to add songs to
sp = spotipy.Spotify(token)
user_id = sp.me()['id']
playlist = sp.user_playlist_create(user_id, name=f"{book_name} recommendations", public=True)

try:
    os.remove(f".cache-{username}")
except:
    pass

result = sp.recommendations(seed_genres=genres, limit=nSongs)
urls = []
uris = []
for i in result['tracks']:
    urls.append(i['external_urls']['spotify'])
    uris.append(i['uri'])

# Adds songs to playlist
# print(urls)
playlist = sp.user_playlist_add_tracks(user_id, playlist["id"], uris)
print(playlist)