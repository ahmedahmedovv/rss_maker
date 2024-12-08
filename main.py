import os
import yaml
from scrapers.scraper_factory import create_scrapers_from_config
from scrapers.rss_generator import RSSGenerator

def ensure_output_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    output_dir = "headlines"
    rss_dir = "rss"
    base_url = "https://rss-maker.onrender.com"  # Update this
    
    ensure_output_dir(output_dir)
    ensure_output_dir(rss_dir)
    
    # Create scrapers from yaml config file
    scrapers = create_scrapers_from_config("config.yaml", output_dir)
    
    # Run all scrapers
    for scraper in scrapers:
        print(f"Running {scraper.site_id} scraper...")
        scraper.get_headlines()
    
    # Generate RSS feeds
    rss_generator = RSSGenerator(output_dir, rss_dir, base_url)
    rss_generator.generate_all_feeds()

if __name__ == "__main__":
    main() 