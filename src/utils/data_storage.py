"""
Data storage utilities for handling comments data
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any

class CommentDataStorage:
    """Handle storage and retrieval of comment data"""
    
    @staticmethod
    def save_comments_to_json(comments: List[Dict[str, Any]], filepath: str) -> bool:
        """
        Save comments to JSON file with proper UTF-8 encoding
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Prepare metadata
            data = {
                "metadata": {
                    "total_comments": len(comments),
                    "created_at": datetime.now().isoformat(),
                    "format_version": "1.0"
                },
                "comments": comments
            }
            
            # Save with proper UTF-8 encoding and ensure_ascii=False for Arabic
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            return False
    
    @staticmethod
    def load_comments_from_json(filepath: str) -> List[Dict[str, Any]]:
        """
        Load comments from JSON file
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data.get("comments", [])
            
        except Exception as e:
            print(f"Error loading from JSON: {e}")
            return []
    
    @staticmethod
    def convert_csv_to_json(csv_filepath: str, json_filepath: str) -> bool:
        """
        Convert existing CSV to JSON format
        """
        try:
            import pandas as pd
            
            # Read CSV with proper encoding
            df = pd.read_csv(csv_filepath, encoding='utf-8')
            
            # Convert to list of dictionaries
            comments = df.to_dict('records')
            
            # Save as JSON
            return CommentDataStorage.save_comments_to_json(comments, json_filepath)
            
        except Exception as e:
            print(f"Error converting CSV to JSON: {e}")
            return False