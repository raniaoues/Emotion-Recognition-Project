"""
Main script to run the YouTube comment scraper
"""
import sys
import os

# Add src to Python path
sys.path.append('src')

from data_collection.youtube_scraper_v2 import main

if __name__ == "__main__":
    main()