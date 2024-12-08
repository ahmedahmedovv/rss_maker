from rfeed import *
from datetime import datetime, timedelta, timezone
import json
import os
from urllib.parse import urljoin
import pytz
import hashlib

class RSSGenerator:
    def __init__(self, json_dir, rss_dir, base_url, max_entries=50, max_age_days=30):
        self.json_dir = json_dir
        self.rss_dir = rss_dir
        self.base_url = base_url
        self.max_entries = max_entries
        self.max_age_days = max_age_days
        self.archive_dir = os.path.join(json_dir, 'archive')
        
        # Ensure directories exist
        for directory in [self.rss_dir, self.archive_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def load_archived_entries(self, site_id):
        archive_file = os.path.join(self.archive_dir, f"{site_id}_archive.json")
        if os.path.exists(archive_file):
            with open(archive_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_archived_entries(self, site_id, entries):
        archive_file = os.path.join(self.archive_dir, f"{site_id}_archive.json")
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)

    def generate_feed(self, json_file):
        # Read current headlines
        with open(os.path.join(self.json_dir, json_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        site_id = data['title'].lower()
        current_time = datetime.now(pytz.UTC)
        
        # Load and combine entries
        archived_entries = self.load_archived_entries(site_id)
        new_entries = [{
            'headline': article['headline'],
            'link': article['link'],
            'id': article.get('id', article['link'] if article['link'] else article['headline']),
            'timestamp': data['timestamp']
        } for article in data['headlines']]
        
        # Combine and deduplicate entries
        all_entries = self._deduplicate_entries(archived_entries + new_entries)
        
        # Filter and sort entries
        valid_entries = self._filter_entries(all_entries, current_time)
        
        # Save updated archive
        self.save_archived_entries(site_id, valid_entries)
        
        # Generate RSS feed
        feed = self._create_feed(data['title'], valid_entries, current_time)
        
        # Save RSS feed
        output_file = os.path.join(self.rss_dir, f"{site_id}.xml")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(feed.rss())

    def _deduplicate_entries(self, entries):
        seen = {}
        unique_entries = []
        
        for entry in entries:
            if entry['id'] not in seen:
                seen[entry['id']] = True
                unique_entries.append(entry)
                
        return unique_entries

    def _filter_entries(self, entries, current_time):
        # Make current_time timezone-aware if it isn't already
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)
        
        max_age = current_time - timedelta(days=self.max_age_days)
        
        return [
            entry for entry in entries
            # Convert entry timestamp to timezone-aware datetime
            if datetime.fromisoformat(entry['timestamp']).replace(tzinfo=timezone.utc) > max_age
        ]
        
        # Sort by date (newest first) and limit count
        return sorted(
            valid_entries,
            key=lambda x: datetime.fromisoformat(x['timestamp']),
            reverse=True
        )[:self.max_entries]

    def _create_feed(self, title, entries, current_time):
        items = []
        for entry in entries:
            item = Item(
                title=entry['headline'],
                link=entry['link'] if entry['link'] else '',
                description=entry['headline'],
                guid=Guid(entry['id']),
                pubDate=datetime.fromisoformat(entry['timestamp'])
            )
            items.append(item)
        
        return Feed(
            title=title,
            link=self.base_url,
            description=f"News headlines from {title}",
            language="en-US",
            lastBuildDate=current_time,
            items=items
        )
        
    def generate_all_feeds(self):
        for filename in os.listdir(self.json_dir):
            if filename.endswith('.json'):
                self.generate_feed(filename) 