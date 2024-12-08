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
    base_url = "https://rss-maker.onrender.com"
    
    ensure_output_dir(output_dir)
    ensure_output_dir(rss_dir)
    
    # Create scrapers from yaml config file
    scrapers = create_scrapers_from_config("config.yaml", output_dir)
    
    # Run all scrapers
    for scraper in scrapers:
        print(f"Running {scraper.site_id} scraper...")
        scraper.get_headlines()
    
    # Generate RSS feeds with limits
    rss_generator = RSSGenerator(
        json_dir=output_dir,
        rss_dir=rss_dir,
        base_url=base_url,
        max_entries=50,  # Keep last 50 entries
        max_age_days=30  # Keep entries for 30 days
    )
    rss_generator.generate_all_feeds()

if __name__ == "__main__":
    main() 