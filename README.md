# 🔧 Social Media & Website Scraper Tools

> **LLM-Powered Web Scraping Tools for Facebook Pages and General Websites**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LangChain](https://img.shields.io/badge/LangChain-Integrated-orange.svg)](https://python.langchain.com/)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.5-red.svg)](https://ai.google.dev/)

A powerful, production-ready toolkit for extracting structured data from Facebook pages and websites using AI-powered extraction with Google Gemini. Built with **Crawl4AI**, **LangChain**, and **Pydantic** for robust, type-safe web scraping.

---

## ✨ Features

### 🎯 Facebook Scraper
- 🤖 **AI-Powered Extraction** - Uses Google Gemini 2.5 Pro for intelligent data extraction
- 📜 **Smart Scrolling** - Automatically scrolls and loads more content
- 🔘 **Button Automation** - Clicks "See More" buttons to expand truncated posts
- ⏰ **Intelligent Timestamp Matching** - Accurately associates posts with their timestamps
- 💬 **Comment Extraction** - Captures comments with author information
- 📊 **Engagement Metrics** - Extracts likes, comments, and shares
- 🔄 **Session Persistence** - Maintains browser sessions (no repeated logins)

### 🌐 Website Scraper
- 🔄 **4-Stage Pipeline** - Progressive HTML refinement for optimal data quality
- 🤖 **LLM-Powered Insights** - Uses Gemini 2.5 Flash for structured data extraction
- 🧹 **Smart Filtering** - Removes CSS, JavaScript, and irrelevant content
- 📊 **Flexible Schema** - Adapts to different website structures
- 💾 **Organized Storage** - Centralized data management in `../data/` directory
- 🔧 **Highly Customizable** - Easy to modify extraction logic and prompts

---

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# Install dependencies
pip install -r requirements.txt
```

### Setup
1. **Clone or download this repository**

2. **Configure API Keys**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Google Gemini API key
   # Get your key from: https://ai.google.dev/
   ```

3. **Create data directories**
   ```bash
   mkdir -p ../data/html_all ../data/html_only ../data/html_only_imp
   ```

4. **For Facebook scraping (first time only)**
   ```bash
   # Run the login script to create a persistent session
   python facebook_c4a_login.py
   ```

### Usage Examples

#### Facebook Scraper
```python
from facebook_basic_scroll import facebook_scraper_tool

# Scrape Facebook page
result = facebook_scraper_tool.invoke({
    "page_url": "https://www.facebook.com/YourTargetPage"
})

# Data saved to: ./data/facebook_scraped_data_YYYYMMDD_HHMMSS.json
```

#### Website Scraper
```python
from websitescraping import website_scraper

# Scrape any website
result = website_scraper.invoke({
    "url": "https://example.com"
})

# Data saved to: ./data/website_scraped_data_sitename_YYYYMMDD_HHMMSS.json
```

---

## 📦 What's Included

### Core Tools
- **`facebook_basic_scroll.py`** - Facebook page scraper with LLM extraction
- **`websitescraping.py`** - Website scraper orchestrator

### Supporting Modules
- **`scraper_1_all_pro.py`** - Stage 1: Full HTML extraction
- **`scraper_2_all_pro_html_only.py`** - Stage 2: HTML-only extraction (no CSS/JS)
- **`scraper_3_imp_pro.py`** - Stage 3: Important content filtering
- **`scraper_4_gemeni_json_gen.py`** - Stage 4: LLM-powered JSON generation

### Configuration
- **`config.py`** - Centralized configuration management
- **`requirements.txt`** - Python dependencies
- **`.env.example`** - Environment variables template
- **`.gitignore`** - Git ignore rules

---

## 🎯 Use Cases

### Facebook Scraper
- 📊 **Social Media Analytics** - Track engagement patterns and trends
- 🔍 **Competitor Analysis** - Monitor competitor social media activity
- 💡 **Content Research** - Gather content ideas and viral patterns
- 😊 **Sentiment Analysis** - Analyze comments and reactions
- 🚀 **Trend Detection** - Identify viral content and influencers

### Website Scraper
- 🏢 **Business Intelligence** - Extract company information and offerings
- 📞 **Lead Generation** - Gather contact information at scale
- 🔬 **Market Research** - Analyze competitor products and services
- 📊 **Data Aggregation** - Collect structured data from multiple sources
- 🎨 **Content Analysis** - Extract features, pricing, and descriptions

---

## 📊 Output Formats

### Facebook Posts
```json
{
  "posts": [
    {
      "post_time": "5 hours ago",
      "content": "Full post text content...",
      "likes_number": "162",
      "comments_number": "82",
      "shares_number": "3",
      "comments": [
        {
          "author": "User Name",
          "text": "Comment text..."
        }
      ]
    }
  ]
}
```

### Website Data (Flexible Schema)
```json
{
  "company_name": "Company Name",
  "services": ["Service 1", "Service 2"],
  "products": ["Product 1", "Product 2"],
  "contact_info": {
    "phone": "+20 123 456 789",
    "email": "info@example.com"
  },
  "pricing": "Pricing information",
  "features": ["Feature 1", "Feature 2"]
}
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file with your API keys:
```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Optional: Alternative LLM providers
# DEEPSEEK_API_KEY=your_deepseek_key
# GROQ_API_KEY=your_groq_key
```

### Facebook Scraper Options
```python
from facebook_basic_scroll import facebook_basic_scroll
import asyncio

result = asyncio.run(facebook_basic_scroll(
    page_url="https://www.facebook.com/Page",
    scroll_count=20,           # Number of scrolls (more = more posts)
    scroll_wait=3,             # Seconds between scrolls
    headless=False,            # Show browser (True = hidden)
    save_debug_files=True      # Save HTML/markdown for debugging
))
```

### Website Scraper Pipeline
The website scraper runs through 4 stages automatically:
1. **Full HTML Download** → `data/html_all/`
2. **HTML Extraction** (no CSS/JS) → `data/html_only/`
3. **Important Content** → `data/html_only_imp/`
4. **LLM Insights** → `data/website_scraped_data_*.json`

---

## 🔌 LangChain Integration

Both tools are designed as LangChain-compatible tools:

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from facebook_basic_scroll import facebook_scraper_tool
from websitescraping import website_scraper

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-latest")

# Add tools to agent
tools = [facebook_scraper_tool, website_scraper]

# Create agent
agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Use in conversation
response = agent_executor.invoke({
    "input": "Scrape the latest posts from TechCrunch's Facebook page"
})
```

---

## 🛠️ Advanced Usage

### Customizing LLM Provider
Both scrapers support multiple LLM providers. Edit the configuration in the respective files:

```python
# In facebook_basic_scroll.py or scraper_4_gemeni_json_gen.py

# Option 1: Google Gemini (default)
llm_config = LLMConfig(
    provider="gemini/gemini-2.5-pro",
    api_token=os.getenv("GOOGLE_API_KEY")
)

# Option 2: DeepSeek
llm_config = LLMConfig(
    provider="deepseek/deepseek-chat",
    api_token=os.getenv("DEEPSEEK_API_KEY")
)

# Option 3: Groq
llm_config = LLMConfig(
    provider="groq/llama-3.3-70b-versatile",
    api_token=os.getenv("GROQ_API_KEY")
)
```

### Modifying Extraction Schema
Edit the Pydantic models to customize extracted fields:

```python
# In facebook_basic_scroll.py
class FacebookPost(BaseModel):
    post_time: Optional[str]
    content: str
    likes_number: Optional[str]
    # Add your custom fields
    sentiment: Optional[str] = Field(description="Post sentiment")
    hashtags: Optional[List[str]] = Field(description="Hashtags used")
```

### Batch Processing
```python
from websitescraping import website_scraper

urls = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
]

results = []
for url in urls:
    result = website_scraper.invoke({"url": url})
    results.append(result)
```

---

## 🐛 Troubleshooting

### Common Issues

**Problem**: "GOOGLE_API_KEY not found"  
**Solution**: Create a `.env` file with your API key (see Setup section)

**Problem**: "Redirected to login - session expired" (Facebook)  
**Solution**: Run `python facebook_c4a_login.py` to re-authenticate

**Problem**: "No content extracted by LLM"  
**Solution**: 
- Set `headless=False` to watch browser behavior
- Check `save_debug_files=True` to inspect HTML/markdown
- Verify your API key is valid and has quota

**Problem**: "File not found" errors (Website scraper)  
**Solution**: Create data directories:
```bash
mkdir -p ../data/html_all ../data/html_only ../data/html_only_imp
```

### Debug Mode
Enable verbose logging and debug files:
```python
result = asyncio.run(facebook_basic_scroll(
    page_url="https://www.facebook.com/Page",
    headless=False,           # Watch browser
    save_debug_files=True,    # Save HTML/markdown
    verbose=True              # Detailed logs
))
```

---

## 📈 Performance

- **Facebook Scraper**: ~30-60 seconds for 20 posts
- **Website Scraper**: ~10-20 seconds per website
- **Memory Usage**: ~200-500 MB during execution
- **Storage**: ~1-5 MB per scraped page

### Optimization Tips
- Use `headless=True` for faster Facebook scraping
- Reduce `scroll_wait` for quicker scrolling (but less reliable)
- Disable `save_debug_files` in production
- Cache results to avoid re-scraping

---

## 🔒 Legal & Ethical Considerations

⚠️ **IMPORTANT**: This tool is provided for educational and research purposes.

### Responsibilities
- ✅ **Review Terms of Service** - Always check target websites' ToS and robots.txt
- ✅ **Respect Rate Limits** - Don't overload servers with requests
- ✅ **Handle Data Responsibly** - Comply with data privacy laws (GDPR, CCPA)
- ✅ **Facebook Policy** - Follow Facebook's Platform Policy when scraping
- ✅ **Ethical Use** - Don't use for malicious purposes or harassment

### Disclaimer
The authors and contributors are not responsible for any misuse of this software or legal consequences arising from its use. Users are solely responsible for ensuring their use complies with all applicable laws and terms of service.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/scraper-tools.git
cd scraper-tools

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run tests (if available)
pytest
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Crawl4AI** - Powerful web crawling framework
- **LangChain** - LLM application framework
- **Google Gemini** - AI-powered data extraction
- **Pydantic** - Data validation and settings management

---

## 📧 Contact & Support

For questions, issues, or suggestions:
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/scraper-tools/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/scraper-tools/discussions)
- 📧 **Email**: your.email@example.com

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ for the NTI Final Project**

*Last Updated: November 2025*
