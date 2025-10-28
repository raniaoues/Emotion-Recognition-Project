# 🚀 Quick Setup Guide

## 📋 Prerequisites
- Python 3.8+
- YouTube Data API v3 key

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Copy your API key

### 3. Configure API Key
Edit `src/utils/config_v2.py`:
```python
YOUTUBE_API_KEY = "paste-your-api-key-here"
```

### 4. Run Collection
```bash
python run_smart_scraper.py
```

### 5. Check Results
```bash
# View collected data
python -c "import json; print(json.load(open('data/tunisian_youtube_comments.json'))['metadata'])"
```

## 🎯 Expected Output
```
🚀 Starting SMART YouTube comment collection...
📂 Category: social
🔍 Searching: عائلة تونسية
   ✅ 15 quality comments from abc123
📊 social: 50 comments collected
...
✅ Successfully saved 250 comments to data/tunisian_youtube_comments.json
```

## 🔧 Troubleshooting
- **API Quota Exceeded**: Wait 24h or use different API key
- **No Comments Found**: Check internet connection and API key
- **Import Errors**: Run `pip install -r requirements.txt`