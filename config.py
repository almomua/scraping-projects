"""
Configuration file for Scraper Tools
Load API keys from environment variables for security
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys - Load from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Validate required keys
if not GOOGLE_API_KEY:
    raise ValueError(
        "❌ GOOGLE_API_KEY not found in environment variables!\n"
        "Please create a .env file (copy from .env.example) and add your API key.\n"
        "Get your key from: https://ai.google.dev/"
    )

# Facebook Scraper Configuration
FACEBOOK_CONFIG = {
    "scroll_count": 20,
    "scroll_wait": 3,
    "headless": False,
    "session_dir": "./facebook_session_c4a",
    "session_id": "facebook_c4a_session",
    "save_debug_files": False  # Set to True for debugging
}

# Website Scraper Configuration
WEBSITE_CONFIG = {
    "model": "gemini-2.5-flash",
    "temperature": 0.2
}

# Data directories
DATA_DIRS = {
    "base": "./data",
    "html_all": "./data/html_all",
    "html_only": "./data/html_only",
    "html_only_imp": "./data/html_only_imp"
}

# Create data directories if they don't exist
for dir_path in DATA_DIRS.values():
    os.makedirs(dir_path, exist_ok=True)

print("✅ Configuration loaded successfully!")
print(f"   Google API Key: {'✓ Set' if GOOGLE_API_KEY else '✗ Missing'}")

