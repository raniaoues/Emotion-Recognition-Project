# 🇹🇳 Tunisian Emotion Recognition Dataset

> **Smart data collection system for Tunisian Arabic emotion recognition using YouTube comments**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](README.md)

---

## 🎯 **Project Overview**

This project collects **high-quality Tunisian Arabic comments** from YouTube for emotion recognition research. It ensures **authenticity**, **diversity**, and **quality** through intelligent filtering and categorization.

### 📊 **Dataset Characteristics**
- **Target**: ~112 characters, 19 tokens per comment (similar to social media posts)
- **Languages**: Tunisian Arabic dialect
- **Categories**: 5 balanced categories covering daily Tunisian life
- **Quality**: Automated Tunisian dialect detection + content filtering

---

## 🏗️ **Project Structure**

```
EmotionRecogn/
├── 📁 src/
│   ├── 🔧 utils/
│   │   ├── config_v2.py           # 🎛️ Configuration & search queries
│   │   ├── tunisian_detector.py   # 🇹🇳 Tunisian dialect detection
│   │   ├── text_processor.py      # 📝 Arabic text processing
│   │   └── data_storage.py        # 💾 JSON storage utilities
│   └── 📊 data_collection/
│       └── smart_scraper.py       # 🤖 Intelligent YouTube scraper
├── 📁 data/
│   └── tunisian_youtube_comments.json  # 📋 Collected dataset
├── 🚀 run_smart_scraper.py        # ▶️ Main execution script
├── 📋 requirements.txt            # 📦 Dependencies
└── 📖 README.md                   # 📚 This file
```

---

## 🚀 **Quick Start**

### 1️⃣ **Installation**
```bash
# Clone the repository
git clone <your-repo-url>
cd EmotionRecogn

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ **Configuration**
Update your YouTube API key in `src/utils/config_v2.py`:
```python
YOUTUBE_API_KEY = "your-api-key-here"
```

### 3️⃣ **Run Data Collection**
```bash
python run_smart_scraper.py
```

### 4️⃣ **View Results**
```bash
# Check collected data
cat data/tunisian_youtube_comments.json
```

---

## 🎯 **Data Collection Strategy**

### 📂 **5 Balanced Categories**

| Category | Description |
|----------|-------------|
| 🏠 **Social** | Family, friends, work, school |
| 🌅 **Daily Life** | Celebrations, food, local events |
| 🎬 **Pop Culture** | Movies, TV, music, sports |
| 😊 **Emotions** | Direct emotional expressions |
| 📰 **Current Events** | News, politics, local issues |

### 🔍 **Quality Assurance**

✅ **Tunisian Dialect Detection**
- Custom dialect detector with 200+ Tunisian-specific words
- Cultural references (cities, celebrities, sports teams)
- Minimum Tunisian score: 0.3/1.0

✅ **Diversity Control**
- Max 20 comments per video (prevents over-sampling)
- Randomized video selection
- Balanced category distribution

✅ **Content Quality**
- Length: 3-500 characters
- Meaningful content (not just emojis)
- Automatic text cleaning and normalization

---

## 📊 **Sample Output**

```json
{
  "metadata": {
    "total_comments": 250,
    "created_at": "2024-01-15T10:30:00",
    "format_version": "1.0"
  },
  "comments": [
    {
      "text": "برشا فرحان بهاذ الخبر الله يوفقكم",
      "author": "@TunisianUser123",
      "date": "2024-01-15T08:15:30+00:00",
      "likes": 5,
      "video_id": "abc123xyz",
      "category": "emotions",
      "tunisian_score": 0.85,
      "char_count": 35,
      "word_count": 7
    }
  ]
}
```

---

## 🔧 **Extending the Project**

### 🐦 **Adding Twitter Support**
```python
# Add to requirements.txt
tweepy==4.14.0

# Create new scraper in src/data_collection/
class TwitterScraper:
    def __init__(self, api_keys):
        # Twitter API setup
        pass
```

### 📘 **Adding Facebook Support**
```python
# Add to requirements.txt  
facebook-sdk==3.1.0

# Extend existing architecture
class FacebookScraper:
    def collect_posts(self):
        # Facebook posts collection
        pass
```

### 🎛️ **Customizing Search Queries**
Edit `src/utils/config_v2.py`:
```python
TUNISIAN_SEARCH_QUERIES = {
    'your_category': [
        "your_query_1",
        "your_query_2"
    ]
}
```

---

## 📈 **Statistics & Monitoring**

The scraper provides real-time statistics:

```
📈 COLLECTION STATISTICS
==================================================
Total comments: 250

📂 By Category:
  social: 50 (20.0%)
  daily_life: 50 (20.0%)
  pop_culture: 50 (20.0%)
  emotions: 50 (20.0%)
  current_events: 50 (20.0%)

📝 Text Statistics:
  Avg characters: 112.3
  Avg words: 18.7
  Avg Tunisian score: 0.654

🎥 Video Diversity: 45 unique videos
```

---

## 🤝 **Contributing**

### 🔄 **Development Workflow**
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/new-scraper`
3. **Add** your scraper following the existing architecture
4. **Test** with small datasets first
5. **Submit** a pull request

### 📋 **Adding New Data Sources**
1. Create scraper in `src/data_collection/`
2. Follow the interface pattern:
   ```python
   class YourScraper:
       def collect_comments(self) -> List[Dict[str, Any]]:
           # Return standardized comment format
           pass
   ```
3. Update `config_v2.py` with new queries
4. Add dependencies to `requirements.txt`

---

## 📞 **Support & Contact**

- 🐛 **Issues**: [GitHub Issues](your-repo-url/issues)
- 💬 **Discussions**: [GitHub Discussions](your-repo-url/discussions)
- 📧 **Email**: your-email@example.com

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**🇹🇳 Built with ❤️ for Tunisian NLP Research**

[![GitHub stars](https://img.shields.io/github/stars/your-username/EmotionRecogn.svg?style=social&label=Star)](https://github.com/your-username/EmotionRecogn)
[![GitHub forks](https://img.shields.io/github/forks/your-username/EmotionRecogn.svg?style=social&label=Fork)](https://github.com/your-username/EmotionRecogn/fork)

</div>