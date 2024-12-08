from rfeed import *
from datetime import datetime
import json
import os
from urllib.parse import urljoin
import pytz

class RSSGenerator:
    def __init__(self, json_dir, rss_dir, base_url):
        self.json_dir = json_dir
        self.rss_dir = rss_dir
        self.base_url = base_url
        
        if not os.path.exists(rss_dir):
            os.makedirs(rss_dir)
    
    def generate_feed(self, json_file):
        # Read JSON file
        with open(os.path.join(self.json_dir, json_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create RSS items
        items = []
        for article in data['headlines']:
            # Use headline as guid if no link available
            guid = article['link'] if article['link'] else article['headline']
            
            item = Item(
                title=article['headline'],
                link=article['link'] if article['link'] else '',
                description=article['headline'],
                guid=Guid(guid),
                pubDate=datetime.fromisoformat(data['timestamp'])
            )
            items.append(item)
        
        # Create feed
        feed = Feed(
            title=data['title'],
            link=self.base_url,
            description=f"News headlines from {data['title']}",
            language="en-US",
            lastBuildDate=datetime.now(pytz.UTC),
            items=items
        )
        
        # Save RSS feed
        output_file = os.path.join(self.rss_dir, f"{data['title'].lower()}.xml")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(feed.rss())
        
    def generate_all_feeds(self):
        for filename in os.listdir(self.json_dir):
            if filename.endswith('.json'):
                self.generate_feed(filename) 