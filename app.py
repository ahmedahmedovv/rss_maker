from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Get list of RSS feeds from rss directory
    rss_dir = "rss"
    rss_files = []
    
    if os.path.exists(rss_dir):
        for file in os.listdir(rss_dir):
            if file.endswith('.xml'):
                feed_name = file[:-4].capitalize()  # Remove .xml and capitalize
                rss_files.append({
                    'name': feed_name,
                    'url': f'/rss/{file}'
                })
    
    return render_template('index.html', feeds=rss_files)

if __name__ == '__main__':
    app.run(debug=True) 