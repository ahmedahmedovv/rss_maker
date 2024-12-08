from abc import ABC, abstractmethod
from datetime import datetime
import os
import json

class NewsScraper(ABC):
    def __init__(self, output_dir="headlines"):
        self.output_dir = output_dir
        
    @abstractmethod
    def get_headlines(self):
        pass
        
    def save_to_json(self, title, headlines_with_links):
        filename = os.path.join(self.output_dir, f"{title.lower()}.json")
        data = {
            "title": title,
            "headlines": [
                {
                    "headline": headline,
                    "link": link,
                    "id": self._generate_id(headline, link)
                }
                for headline, link in headlines_with_links
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def _generate_id(self, headline, link):
        # Use link as ID if available, otherwise use headline
        return link if link else headline