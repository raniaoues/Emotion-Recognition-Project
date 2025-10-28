"""
Run the smart YouTube comment scraper
"""
import sys
import os

# Add src to Python path
sys.path.append('src')

from data_collection.smart_scraper import main

if __name__ == "__main__":
    main()