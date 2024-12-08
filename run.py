import subprocess
import sys
from main import main as run_scraper

def run():
    # First run the scraper
    print("Running scrapers...")
    run_scraper()
    
    # Then start the web server
    print("Starting web server...")
    subprocess.run(["gunicorn", "-c", "gunicorn_config.py", "app:app"])

if __name__ == "__main__":
    run() 