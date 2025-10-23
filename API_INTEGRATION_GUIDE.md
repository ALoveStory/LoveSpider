# 🔑 API Integration Guide

## Current Status

Your Spider Search Engine is running in **DEMO MODE** with sample results.

### Why Demo Mode?

Both Google and DuckDuckGo block automated scraping with CAPTCHA challenges. To get real search results, you need to use official APIs.

---

## Option 1: Google Custom Search API (Recommended)

### ✅ Pros:
- Official and legal
- 100 free queries per day
- Reliable results
- Good documentation

### ❌ Cons:
- Limited free tier
- Requires setup and API key

### Setup Steps:

1. **Get API Credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable "Custom Search API"
   - Create credentials (API Key)
   - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
   - Create a new search engine
   - Get your Search Engine ID (cx parameter)

2. **Install Required Package:**
   ```bash
   pip install google-api-python-client
   ```

3. **Update `app.py`:**
   ```python
   from googleapiclient.discovery import build
   import os
   
   # Add at the top of app.py
   GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'your-api-key-here')
   GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID', 'your-search-engine-id')
   
   def search_google_api(query):
       """Use Google Custom Search API"""
       try:
           service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
           result = service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=10).execute()
           
           links = []
           if 'items' in result:
               for item in result['items']:
                   links.append(item['link'])
           
           return links
       except Exception as e:
           print(f"Error with Google API: {e}")
           return []
   
   # Replace the search_google function
   def search_google(query):
       return search_google_api(query)
   ```

4. **Set Environment Variables:**
   ```bash
   export GOOGLE_API_KEY="your-actual-api-key"
   export GOOGLE_CSE_ID="your-actual-search-engine-id"
   ```

---

## Option 2: Bing Search API

### ✅ Pros:
- 1,000 free queries per month
- Microsoft product, good support
- Easy to set up

### ❌ Cons:
- Requires Azure account
- Less popular than Google

### Setup Steps:

1. **Get API Key:**
   - Go to [Azure Portal](https://portal.azure.com/)
   - Create "Bing Search v7" resource
   - Copy your API key

2. **Install Package:**
   ```bash
   pip install azure-cognitiveservices-search-websearch
   ```

3. **Update `app.py`:**
   ```python
   from azure.cognitiveservices.search.websearch import WebSearchClient
   from msrest.authentication import CognitiveServicesCredentials
   import os
   
   BING_API_KEY = os.getenv('BING_API_KEY', 'your-bing-api-key')
   
   def search_bing_api(query):
       """Use Bing Search API"""
       try:
           client = WebSearchClient(
               endpoint="https://api.bing.microsoft.com",
               credentials=CognitiveServicesCredentials(BING_API_KEY)
           )
           
           web_data = client.web.search(query=query, count=10)
           links = []
           
           if web_data.web_pages and web_data.web_pages.value:
               for page in web_data.web_pages.value:
                   links.append(page.url)
           
           return links
       except Exception as e:
           print(f"Error with Bing API: {e}")
           return []
   
   def search_google(query):
       return search_bing_api(query)
   ```

---

## Option 3: SerpAPI (Easiest but Paid)

### ✅ Pros:
- Handles all the scraping complexity
- Supports multiple search engines
- Very easy to use
- 100 free searches/month

### ❌ Cons:
- Costs money after free tier
- Third-party service

### Setup Steps:

1. **Sign up:**
   - Go to [SerpAPI](https://serpapi.com/)
   - Sign up for free account
   - Get your API key

2. **Install Package:**
   ```bash
   pip install google-search-results
   ```

3. **Update `app.py`:**
   ```python
   from serpapi import GoogleSearch
   import os
   
   SERPAPI_KEY = os.getenv('SERPAPI_KEY', 'your-serpapi-key')
   
   def search_serpapi(query):
       """Use SerpAPI for Google search results"""
       try:
           params = {
               "q": query,
               "api_key": SERPAPI_KEY,
               "num": 10
           }
           
           search = GoogleSearch(params)
           results = search.get_dict()
           
           links = []
           if 'organic_results' in results:
               for result in results['organic_results']:
                   links.append(result['link'])
           
           return links
       except Exception as e:
           print(f"Error with SerpAPI: {e}")
           return []
   
   def search_google(query):
       return search_serpapi(query)
   ```

---

## Option 4: Browser Automation (Advanced)

### Use Selenium or Playwright to control a real browser

### ⚠️ Warning:
- Much slower
- Resource-intensive
- Can still be detected
- Requires headless browser setup

### Quick Example with Selenium:

```bash
pip install selenium webdriver-manager
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_with_selenium(query):
    """Use Selenium to automate browser"""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        driver.get(f"https://www.google.com/search?q={query}")
        time.sleep(2)  # Wait for results
        
        links = []
        results = driver.find_elements(By.CSS_SELECTOR, 'a')
        
        for link in results:
            href = link.get_attribute('href')
            if href and href.startswith('http') and 'google.com' not in href:
                links.append(href)
        
        driver.quit()
        return links[:10]
    except Exception as e:
        print(f"Selenium error: {e}")
        return []
```

---

## Recommended Path

For testing and learning:
1. **Start with Demo Mode** ✅ (Already set up!)
2. **Try SerpAPI free tier** - Easiest to get working
3. **Move to Google Custom Search API** - Best for production

For serious production use:
1. **Google Custom Search API** for quality
2. **Bing Search API** as backup
3. Consider paid SerpAPI for high volume

---

## Testing Your Integration

Once you implement an API, test it:

```bash
# Test via curl
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"test query"}'

# Test via Python
python3 << EOF
import requests
response = requests.post(
    'http://localhost:8000/search',
    json={'query': 'test query'}
)
print(response.json())
EOF
```

---

## Cost Comparison

| Service | Free Tier | After Free | Best For |
|---------|-----------|------------|----------|
| **Google Custom Search** | 100/day | $5 per 1K | Most projects |
| **Bing Search** | 1,000/month | $3-7 per 1K | Budget-conscious |
| **SerpAPI** | 100/month | $50/month (5K searches) | Convenience |
| **Scraping (Demo)** | Unlimited | N/A | Testing only |

---

## Need Help?

Check out these resources:
- [Google CSE Docs](https://developers.google.com/custom-search/v1/overview)
- [Bing Search API Docs](https://docs.microsoft.com/en-us/bing/search-apis/)
- [SerpAPI Docs](https://serpapi.com/search-api)

---

## Current Demo Mode

The app currently returns sample results for these keywords:
- **"python"** - Python programming resources
- **"flask"** - Flask framework resources  
- **"web scraping"** - Web scraping tutorials
- **Any other query** - Generic placeholder results

This lets you test the interface while you set up a real API!

