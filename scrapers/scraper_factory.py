import yaml
from .base_scraper import NewsScraper
import requests
from lxml import html
import json

class DynamicScraper(NewsScraper):
    def __init__(self, site_id, url, selector, output_dir="headlines"):
        super().__init__(output_dir)
        self.site_id = site_id
        self.url = url
        self.selector = selector
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_headlines(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            
            tree = html.fromstring(response.content)
            if '//' in self.selector:
                headlines = tree.xpath(f"{self.selector}//text()")
                links = []  # Handle xpath case if needed
            else:
                elements = tree.cssselect(self.selector)
                headlines = []
                links = []
                
                for element in elements:
                    # Get headline text
                    headline = element.text_content().strip()
                    if headline:
                        headlines.append(headline)
                        
                        # Try to get link - first check if element is <a> or has parent <a>
                        link = None
                        if element.tag == 'a':
                            link = element.get('href')
                        else:
                            parent_a = element.xpath('./ancestor::a[1]')
                            if parent_a:
                                link = parent_a[0].get('href')
                        
                        # Make link absolute if it's relative
                        if link and not link.startswith(('http://', 'https://')):
                            link = requests.compat.urljoin(self.url, link)
                        
                        links.append(link if link else '')
            
            # Filter out empty headlines
            headlines_with_links = [(h, l) for h, l in zip(headlines, links) if h.strip()]
            
            title = self.site_id.capitalize()
            self.save_to_markdown(title, headlines_with_links)
            self.save_to_json(title, headlines_with_links)
            
            return headlines_with_links
            
        except Exception as e:
            print(f"Error scraping {self.site_id}: {e}")
            return []

def create_scrapers_from_config(config_file, output_dir="headlines"):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
        
    scrapers = []
    for site in config['sites']:
        scrapers.append(DynamicScraper(
            site_id=site['id'],
            url=site['url'],
            selector=site['selector'],
            output_dir=output_dir
        ))
    
    return scrapers 