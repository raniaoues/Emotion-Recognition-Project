"""
Smart YouTube Comment Scraper with Tunisian detection and diversity control
"""
import os
import sys
import googleapiclient.discovery
from datetime import datetime, timedelta
from dateutil import parser
from langdetect import detect
from typing import List, Dict, Any, Optional
from collections import defaultdict
import random

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.text_processor import ArabicTextProcessor
from utils.data_storage import CommentDataStorage
from utils.tunisian_detector import TunisianDialectDetector
from utils.config_v2 import Config

class SmartYouTubeCommentScraper:
    """Smart scraper with Tunisian detection and diversity control"""
    
    def __init__(self, api_key: str):
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=api_key
        )
        self.text_processor = ArabicTextProcessor()
        self.storage = CommentDataStorage()
        self.tunisian_detector = TunisianDialectDetector()
        self.collected_stats = defaultdict(int)
        self.video_comment_counts = defaultdict(int)

    def get_video_ids(self, query: str, max_results: int = 10) -> List[str]:
        """Search for videos and return their IDs"""
        published_after = (datetime.now() - timedelta(days=Config.DEFAULT_SEARCH_PERIOD_DAYS)).isoformat() + "Z"

        request = self.youtube.search().list(
            part="id,snippet",
            q=query,
            type="video",
            maxResults=max_results,
            publishedAfter=published_after,
            regionCode="TN",
            relevanceLanguage="ar"
        )

        response = request.execute()
        return [item["id"]["videoId"] for item in response.get("items", []) 
                if item["id"]["kind"] == "youtube#video"]

    def is_quality_comment(self, text: str) -> bool:
        """Check if comment meets quality criteria"""
        # Length check
        if len(text) < Config.MIN_COMMENT_LENGTH or len(text) > Config.MAX_COMMENT_LENGTH:
            return False
        
        # Tunisian dialect check
        tunisian_score = self.tunisian_detector.calculate_tunisian_score(text)
        if tunisian_score < Config.TUNISIAN_THRESHOLD:
            return False
        
        # Not just emojis or repeated characters
        clean_text = ''.join(c for c in text if c.isalpha())
        if len(clean_text) < 3:
            return False
        return True

    def get_comments_with_quality_control(self, video_id: str, category: str, 
                                        max_results: int = 80) -> List[Dict[str, Any]]:
        """Get comments with quality control and diversity"""
        comments = []
        
        # Skip if we already have too many comments from this video
        if self.video_comment_counts[video_id] >= Config.MAX_COMMENTS_PER_VIDEO:
            return comments

        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results,
                textFormat="plainText"
            )

            while request and len(comments) < Config.MAX_COMMENTS_PER_VIDEO:
                response = request.execute()

                for item in response.get("items", []):
                    comment_data = item["snippet"]["topLevelComment"]["snippet"]
                    text = comment_data["textDisplay"]

                    # Quality checks
                    if self.is_quality_comment(text):
                        # Clean and normalize the text
                        cleaned_text = self.text_processor.clean_comment_text(text)
                        
                        # Get Tunisian indicators for metadata
                        tunisian_indicators = self.tunisian_detector.get_tunisian_indicators(text)
                        tunisian_score = self.tunisian_detector.calculate_tunisian_score(text)
                        
                        comment = {
                            "text": cleaned_text,
                            "author": comment_data["authorDisplayName"],
                            "date": comment_data["publishedAt"],
                            "likes": comment_data["likeCount"],
                            "video_id": video_id,
                            "category": category,
                            "tunisian_score": tunisian_score,
                            "tunisian_indicators": tunisian_indicators,
                            "char_count": len(cleaned_text),
                            "word_count": len(cleaned_text.split())
                        }
                        
                        comments.append(comment)
                        self.video_comment_counts[video_id] += 1
                        
                        if len(comments) >= Config.MAX_COMMENTS_PER_VIDEO:
                            break

                request = self.youtube.commentThreads().list_next(request, response)

        except Exception as e:
            print(f"Error getting comments for video {video_id}: {str(e)}")

        return comments

    def collect_diverse_comments(self, target_per_category: int = 100) -> List[Dict[str, Any]]:
        """Collect diverse comments across all categories"""
        all_comments = []
        
        print("🎯 Starting diverse comment collection...")
        
        for category, queries in Config.TUNISIAN_SEARCH_QUERIES.items():
            print(f"\n📂 Category: {category}")
            category_comments = []
            
            # Shuffle queries for randomness
            shuffled_queries = queries.copy()
            random.shuffle(shuffled_queries)
            
            for query in shuffled_queries:
                if len(category_comments) >= target_per_category:
                    break
                    
                print(f"🔍 Searching: {query}")
                video_ids = self.get_video_ids(query, max_results=5)
                
                # Shuffle videos for diversity
                random.shuffle(video_ids)
                
                for video_id in video_ids:
                    if len(category_comments) >= target_per_category:
                        break
                        
                    comments = self.get_comments_with_quality_control(
                        video_id, category, max_results=30
                    )
                    category_comments.extend(comments)
                    
                    if comments:
                        print(f"   ✅ {len(comments)} quality comments from {video_id}")
            
            print(f"📊 {category}: {len(category_comments)} comments collected")
            all_comments.extend(category_comments)
            self.collected_stats[category] = len(category_comments)
        
        return all_comments

    def print_collection_stats(self, comments: List[Dict[str, Any]]):
        """Print detailed collection statistics"""
        print("\n📈 COLLECTION STATISTICS")
        print("=" * 50)
        
        # Overall stats
        total_comments = len(comments)
        print(f"Total comments: {total_comments}")
        
        # Category breakdown
        print("\n📂 By Category:")
        for category, count in self.collected_stats.items():
            percentage = (count / total_comments * 100) if total_comments > 0 else 0
            print(f"  {category}: {count} ({percentage:.1f}%)")
        
        # Text statistics
        if comments:
            char_counts = [c['char_count'] for c in comments]
            word_counts = [c['word_count'] for c in comments]
            tunisian_scores = [c['tunisian_score'] for c in comments]
            
            print(f"\n📝 Text Statistics:")
            print(f"  Avg characters: {sum(char_counts)/len(char_counts):.1f}")
            print(f"  Avg words: {sum(word_counts)/len(word_counts):.1f}")
            print(f"  Avg Tunisian score: {sum(tunisian_scores)/len(tunisian_scores):.3f}")
        
        # Video diversity
        unique_videos = len(set(c['video_id'] for c in comments))
        print(f"\n🎥 Video Diversity: {unique_videos} unique videos")

    def save_comments(self, comments: List[Dict[str, Any]], filepath: str) -> bool:
        """Save comments to JSON file"""
        return self.storage.save_comments_to_json(comments, filepath)

def main():
    """Main execution function"""
    scraper = SmartYouTubeCommentScraper(Config.YOUTUBE_API_KEY)
    
    print("🚀 Starting SMART YouTube comment collection...")
    
    # Collect diverse comments (50 per category for testing)
    comments = scraper.collect_diverse_comments(target_per_category=50)
    
    # Print statistics
    scraper.print_collection_stats(comments)
    
    # Ensure data directory exists
    Config.ensure_data_dir()
    
    # Save to JSON
    success = scraper.save_comments(comments, Config.COMMENTS_JSON_FILE)
    
    if success:
        print(f"\n✅ Successfully saved {len(comments)} comments to {Config.COMMENTS_JSON_FILE}")
    else:
        print("\n❌ Failed to save comments")

if __name__ == "__main__":
    main()