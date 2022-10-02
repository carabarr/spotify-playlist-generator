from flask import Flask, render_template, Markup, request, redirect, url_for
from string import Template
import requests
import get_genres
import getRecommendation

app = Flask(__name__)

def is_url_ok(url):
    return 200 == requests.head(url).status_code


IFRAME_TEMPLATE = Template("""
    <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/$playlist_id?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>""")

def get_playlist(title):
    return getRecommendation.recommend(title, get_genres.genres(title), 20) 

 
@app.route('/')
def form():
    text = """
    <div class="instructions">
    <p> Please ensure that you are logged out of all Spotify accounts on your computer. When prompted to log in, please use the following to log in:</p>
    <ul>
        <li>Email: RecommendationSpotify@gmail.com</li>
        <li>Password: RecommendationSpotify</li>
    </ul>
    </div>
    """
    text = Markup(text)
    return render_template('index.html', description=text)
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        title = request.form['bookTitle']
        pid = get_playlist(title)
        playlist_url = 'https://open.spotify.com/playlist/' + pid

        if True == is_url_ok(playlist_url):
            iframe = Markup(IFRAME_TEMPLATE.substitute(playlist_id=pid))
        else:
            return "request failed!"
        return render_template('index.html', embed = iframe)
 
 
app.run(host='localhost', port=5000, use_reloader=True, debug=True)