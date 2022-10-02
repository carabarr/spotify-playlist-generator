from flask import Flask, render_template, Markup, request, redirect, url_for
from string import Template
import requests

app = Flask(__name__)

def is_url_ok(url):
    return 200 == requests.head(url).status_code


IFRAME_TEMPLATE = Template("""
    <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/$playlist_id?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>""")

 
@app.route('/')
def form():
    return render_template('index.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form['bookTitle']
        pid = "5CDAopvNdx8qWXLDsN75Jr"
        playlist_url = 'https://open.spotify.com/playlist/' + pid

        if True == is_url_ok(playlist_url):
            iframe = Markup(IFRAME_TEMPLATE.substitute(playlist_id=pid))
        else:
            return "request failed!"
        return render_template('index.html', embed = iframe)
 
 
app.run(host='localhost', port=5000, use_reloader=True, debug=True)