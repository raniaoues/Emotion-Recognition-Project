"""
Convert existing CSV file to properly formatted JSON
"""
import sys
import os
sys.path.append('src')

from utils.text_processor import ArabicTextProcessor
from utils.data_storage import CommentDataStorage
import pandas as pd

def convert_existing_csv():
    """Convert the existing CSV to JSON with proper Arabic handling"""
    
    csv_file = "data/tunisian_youtube_comments.csv"
    json_file = "data/tunisian_youtube_comments.json"
    
    try:
        # Read the CSV file
        print("Reading CSV file...")
        df = pd.read_csv(csv_file, encoding='utf-8')
        
        # Process each comment
        print("Processing Arabic text...")
        processed_comments = []
        
        for _, row in df.iterrows():
            # Clean and normalize the Arabic text
            cleaned_text = ArabicTextProcessor.clean_comment_text(row['text'])
            
            comment = {
                "text": cleaned_text,
                "author": row['author'],
                "date": row['date'],
                "likes": int(row['likes']),
                "video_id": row['video_id']
            }
            processed_comments.append(comment)
        
        # Save to JSON
        print("Saving to JSON...")
        success = CommentDataStorage.save_comments_to_json(processed_comments, json_file)
        
        if success:
            print(f"✅ Successfully converted {len(processed_comments)} comments to {json_file}")
            
            # Show a few examples
            print("\nFirst 3 comments:")
            for i, comment in enumerate(processed_comments[:3]):
                print(f"{i+1}. Author: {comment['author']}")
                print(f"   Text: {comment['text']}")
                print(f"   Likes: {comment['likes']}")
                print()
        else:
            print("❌ Failed to save JSON file")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    convert_existing_csv()