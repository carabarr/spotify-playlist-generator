# Wordplay
A Spotify Playlist generator based on the genres of a given book.
## Overview
Wordplay is a web app that takes the title of a book, searches OpenLibrary for the genres associated with it, and generates a Spotify playlist based on the semantic association between the book genres and music genres.

## Usage
The web app has one input box where you can type the title of the book you want to create a playlist for. Since authorization to use the full API can take up to 6 weeks to get, the users need to logout of their accounts and login onto a temporary spotify account when prompted. The credentials for that are in the homepage, right below the input box. 


## Setup

Must download the following packages: 
`flask v2.2.2, requests v2.22.0, spacy v3.4.1, spotipy v2.20.0`
Additionally must run the following command to download a spaCy model:
`python -m spacy download en_core_web_md`
