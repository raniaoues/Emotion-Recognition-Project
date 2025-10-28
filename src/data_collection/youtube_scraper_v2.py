"""
Clean YouTube Comment Scraper with proper Arabic handling and JSON storage
"""
import os
import sys
import googleapiclient.discovery
from datetime import datetime, timedelta
from dateutil import parser
from langdetect import detect
from typing import List, Dict, Any, Optional

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.text_processor import ArabicTextProcessor
from utils.data_storage import CommentDataStorage
from utils.config import Config

class YouTubeCommentScraper:
    """Clean YouTube comment scraper with proper Arabic text handling"""
    
    def __init__(self, api_key: str):
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=api_key
        )
        self.text_processor = ArabicTextProcessor()
        self.storage = CommentDataStorage()

    def get_video_ids(self, query: str, max_results: int = 50, 
                     published_after: Optional[str] = None) -> List[str]:
        """Search for videos and return their IDs"""
        if published_after is None:
            published_after = (datetime.now() - timedelta(days=365)).isoformat() + "Z"

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

    def get_comments(self, video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Get comments for a specific video with proper Arabic handling"""
        comments = []

        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results,
                textFormat="plainText"
            )

            while request:
                response = request.execute()

                for item in response.get("items", []):
                    comment_data = item["snippet"]["topLevelComment"]["snippet"]
                    text = comment_data["textDisplay"]

                    # Check if comment contains Arabic
                    if self._is_arabic_comment(text):
                        # Process and clean the text
                        cleaned_text = self.text_processor.clean_comment_text(text)
                        
                        comments.append({
                            "text": cleaned_text,
                            "author": comment_data["authorDisplayName"],
                            "date": comment_data["publishedAt"],
                            "likes": comment_data["likeCount"],
                            "video_id": video_id
                        })

                request = self.youtube.commentThreads().list_next(request, response)

        except Exception as e:
            print(f"Error getting comments for video {video_id}: {str(e)}")

        return comments

    def _is_arabic_comment(self, text: str) -> bool:
        """Check if comment is in Arabic"""
        try:
            detected_lang = detect(text)
            return (detected_lang in ["ar", "undefined"] or 
                   self.text_processor.is_arabic_text(text))
        except:
            return self.text_processor.is_arabic_text(text)

    def collect_comments(self, search_queries: List[str], 
                        max_videos: int = 10, 
                        max_comments_per_video: int = 100) -> List[Dict[str, Any]]:
        """Collect comments for multiple search queries"""
        all_comments = []

        for query in search_queries:
            print(f"🔍 Searching videos for: {query}")
            video_ids = self.get_video_ids(query, max_results=max_videos)
            print(f"📹 Found {len(video_ids)} videos")

            for i, video_id in enumerate(video_ids, 1):
                print(f"💬 Getting comments from video {i}/{len(video_ids)}: {video_id}")
                comments = self.get_comments(video_id, max_results=max_comments_per_video)
                all_comments.extend(comments)
                print(f"   ✅ Collected {len(comments)} Arabic comments")

        return all_comments

    def save_comments(self, comments: List[Dict[str, Any]], filepath: str) -> bool:
        """Save comments to JSON file"""
        return self.storage.save_comments_to_json(comments, filepath)

def main():
    """Main execution function"""
    # Initialize scraper with config
    scraper = YouTubeCommentScraper(Config.YOUTUBE_API_KEY)
    
    print("🚀 Starting YouTube comment collection...")
    
    # Collect comments using config settings
    comments = scraper.collect_comments(
        Config.TUNISIAN_SEARCH_QUERIES[:3],  # Use first 3 queries for testing
        max_videos=3,
        max_comments_per_video=20
    )
    
    # Ensure data directory exists
    Config.ensure_data_dir()
    
    # Save to JSON
    success = scraper.save_comments(comments, Config.COMMENTS_JSON_FILE)
    
    if success:
        print(f"✅ Successfully saved {len(comments)} comments to {Config.COMMENTS_JSON_FILE}")
    else:
        print("❌ Failed to save comments")

if __name__ == "__main__":
    main()