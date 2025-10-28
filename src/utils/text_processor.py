"""
Text processing utilities for Arabic text handling
"""
import re
import unicodedata

class ArabicTextProcessor:
    """Handle Arabic text processing and normalization"""
    
    @staticmethod
    def normalize_arabic_text(text):
        """
        Normalize Arabic text for proper storage and display
        """
        if not text or not isinstance(text, str):
            return text
            
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Normalize Unicode (NFC normalization)
        text = unicodedata.normalize('NFC', text)
        
        # Remove any control characters that might interfere
        text = re.sub(r'[\u200e\u200f\u202a-\u202e]', '', text)
        
        return text
    
    @staticmethod
    def clean_comment_text(text):
        """
        Clean comment text while preserving Arabic characters and emojis
        """
        if not text:
            return ""
            
        # Normalize the text first
        text = ArabicTextProcessor.normalize_arabic_text(text)
        
        # Remove excessive repeated characters (more than 3 in a row)
        text = re.sub(r'(.)\1{3,}', r'\1\1\1', text)
        
        return text
    
    @staticmethod
    def is_arabic_text(text):
        """
        Check if text contains Arabic characters
        """
        if not text:
            return False
            
        arabic_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
        return bool(re.search(arabic_pattern, text))