import pandas as pd
import re

def fix_arabic_text(text):
    """Fix Arabic text display issues"""
    if pd.isna(text):
        return text
    
    # Remove any reshaping artifacts and normalize
    text = str(text)
    
    # Basic cleanup - remove extra spaces and normalize
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def main():
    # Read the CSV file
    input_file = "data/tunisian_youtube_comments.csv"
    output_file = "data/tunisian_youtube_comments_fixed.csv"
    
    try:
        # Read with proper encoding
        df = pd.read_csv(input_file, encoding='utf-8')
        
        # Fix the text column
        df['text'] = df['text'].apply(fix_arabic_text)
        
        # Save the fixed version
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"Fixed CSV saved to: {output_file}")
        print(f"Total comments: {len(df)}")
        
        # Show first few examples
        print("\nFirst 5 comments (fixed):")
        for i, row in df.head().iterrows():
            try:
                print(f"{i+1}. Text length: {len(row['text'])} characters")
            except:
                print(f"{i+1}. [Arabic text - {len(row['text'])} chars]")
            
    except Exception as e:
        print(f"Error reading file: {e}")
        
        # Try alternative approach
        try:
            print("Trying alternative encoding...")
            df = pd.read_csv(input_file, encoding='utf-8-sig')
            df['text'] = df['text'].apply(fix_arabic_text)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"Successfully fixed and saved to: {output_file}")
        except Exception as e2:
            print(f"Alternative approach failed: {e2}")

if __name__ == "__main__":
    main()