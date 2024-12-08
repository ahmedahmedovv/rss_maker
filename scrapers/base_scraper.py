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
        
    def save_to_markdown(self, title, headlines_with_links):
        filename = os.path.join(self.output_dir, f"{title}.md")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            for headline, link in headlines_with_links:
                if link:
                    f.write(f"- [{headline}]({link})\n")
                else:
                    f.write(f"- {headline}\n") 

    def save_to_json(self, title, headlines_with_links):
        filename = os.path.join(self.output_dir, f"{title}.json")
        data = {
            "title": title,
            "headlines": [
                {
                    "headline": headline,
                    "link": link
                }
                for headline, link in headlines_with_links
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)