from flask import Flask, render_template, send_from_directory, jsonify
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

@app.route('/rss/<path:filename>')
def serve_rss(filename):
    return send_from_directory('rss', filename, mimetype='application/rss+xml')

@app.route('/folder-contents')
def show_folder_contents():
    # Get contents of both folders
    rss_contents = []
    headlines_contents = []
    
    # Check RSS folder
    rss_dir = "rss"
    if os.path.exists(rss_dir):
        rss_contents = [f for f in os.listdir(rss_dir) if f.endswith('.xml')]
    
    # Check headlines folder
    headlines_dir = "headlines"
    if os.path.exists(headlines_dir):
        headlines_contents = [f for f in os.listdir(headlines_dir) if f.endswith('.json')]
    
    return render_template('folder_contents.html', 
                         rss_files=rss_contents,
                         headlines_files=headlines_contents)

@app.route('/headlines/<path:filename>')
def serve_json(filename):
    try:
        # Print debugging information
        print(f"Attempting to serve: {filename}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Files in headlines directory: {os.listdir('headlines')}")
        
        return send_from_directory('headlines', filename, mimetype='application/json')
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return f"Error: {str(e)}", 404

if __name__ == '__main__':
    app.run(debug=True) 