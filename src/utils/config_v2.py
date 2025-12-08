"""
Configuration settings for the emotion recognition project
"""
import os
from typing import List, Dict

class Config:
    """Configuration class for project settings"""
    
    # API Configuration
    YOUTUBE_API_KEY = ""
    
    # Data Collection Settings
    DEFAULT_MAX_VIDEOS = 10
    DEFAULT_MAX_COMMENTS_PER_VIDEO = 20
    DEFAULT_SEARCH_PERIOD_DAYS = 365
    
    # Diversified search strategy for Tunisian content
    TUNISIAN_SEARCH_QUERIES = {
        # Social interactions
        'social': [
            "عائلة تونسية", "أصدقاء تونس", "شغل تونس", "جامعة تونسية",
            "مدرسة تونس",
        ],
        
        # Daily life events
        'daily_life': [
            "عيد تونس", "رمضان تونس"
            "سوق تونس", "شارع تونس", "حي تونسي", "مقهى تونسي"
        ],
        
        # Pop culture
        'pop_culture': [
            "فيلم تونسي", "مسلسل تونسي", "أغنية تونسية", "مهرجان تونس",
            "كرة القدم تونس", "الترجي"
        ],
        
        # Emotions in context
        'emotions': [
            "فرحان تونس",
            "حزين تونس",
            "خايف تونس"
        ],


        # Current events and news
        'current_events': [
            "أخبار تونس", "سياسة تونس", "اقتصاد تونس", "طقس تونس",
            "تعليم تونس", "صحة تونس", "رياضة تونس"
        ]
    }
    
    # File Paths
    DATA_DIR = "data"
    COMMENTS_JSON_FILE = os.path.join(DATA_DIR, "tunisian_youtube_comments.json")
    PROCESSED_DATA_FILE = os.path.join(DATA_DIR, "processed_comments.json")
    
    # Text Processing Settings
    MAX_COMMENT_LENGTH = 500
    MIN_COMMENT_LENGTH = 3
    TARGET_AVG_LENGTH = 112  # characters
    TARGET_AVG_TOKENS = 19   # words
    
    # Quality Control Settings
    TUNISIAN_THRESHOLD = 0.3  # Minimum Tunisian score
    MIN_COMMENTS_PER_CATEGORY = 50
    MAX_COMMENTS_PER_VIDEO = 20  # Avoid over-sampling single videos
    
    @classmethod
    def get_all_queries(cls) -> List[str]:
        """Get all search queries as a flat list"""
        all_queries = []
        for category_queries in cls.TUNISIAN_SEARCH_QUERIES.values():
            all_queries.extend(category_queries)
        return all_queries
    
    @classmethod
    def get_queries_by_category(cls, category: str) -> List[str]:
        """Get queries for a specific category"""
        return cls.TUNISIAN_SEARCH_QUERIES.get(category, [])
    
    @classmethod
    def get_output_path(cls, filename: str) -> str:
        """Get full output path for a file"""
        return os.path.join(cls.DATA_DIR, filename)
    
    @classmethod
    def ensure_data_dir(cls) -> None:
        """Ensure data directory exists"""
        os.makedirs(cls.DATA_DIR, exist_ok=True)
