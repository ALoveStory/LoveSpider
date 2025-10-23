# Author: Antwan Love (ADLJR)
# Flask Web Application for Spider Search Engine

from flask import Flask, render_template, request, jsonify, send_file
import csv
import re
import requests
import io
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = 'your-secret-key-here'


def extract_links_from_response(response):
    """
    Extract links from Google search response
    Returns a list of URLs
    """
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        
        # Method 1: Try extracting from /url?q= pattern (classic Google)
        for link in soup.find_all('a', href=re.compile("/url")):
            html_url = link.get("href")
            if html_url:
                # Clean up the URL
                url = html_url.strip("/url?q=")
                # Remove additional Google parameters
                url = url.split('&')[0]
                if url and url.startswith('http'):
                    links.append(url)
        
        # Method 2: Try direct links (newer Google results)
        if not links:
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                # Filter for actual result links
                if href.startswith('http') and not any(x in href for x in ['google.com', 'webcache', 'accounts.google']):
                    # Skip Google's own links
                    if 'q=' not in href and 'search' not in href:
                        links.append(href)
        
        # Method 3: Extract from cite tags (backup method)
        if not links:
            for cite in soup.find_all('cite'):
                url_text = cite.get_text()
                if url_text:
                    # Construct full URL if needed
                    if not url_text.startswith('http'):
                        url_text = 'https://' + url_text.split(' ›')[0]
                    links.append(url_text)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_links = []
        for link in links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        print(f"DEBUG: Extracted {len(unique_links)} links")
        return unique_links
    except Exception as e:
        print(f"Error extracting links: {e}")
        import traceback
        traceback.print_exc()
        return []


def search_duckduckgo(query):
    """
    Perform DuckDuckGo search and return list of links
    DuckDuckGo is more scraper-friendly than Google
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }
        
        print(f"DEBUG: Searching DuckDuckGo for: {query}")
        
        response = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers=headers,
            timeout=10
        )
        
        print(f"DEBUG: Response status code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = []
            
            # DuckDuckGo HTML structure: results are in <a class="result__url">
            for result in soup.find_all('a', class_='result__url'):
                href = result.get('href')
                if href:
                    # DuckDuckGo uses redirect links, extract the actual URL
                    if 'uddg=' in href:
                        # Extract URL from uddg parameter
                        import urllib.parse
                        parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                        if 'uddg' in parsed:
                            actual_url = parsed['uddg'][0]
                            links.append(actual_url)
                    elif href.startswith('http'):
                        links.append(href)
            
            # Alternative: look for result snippets with data-nrn attribute
            if not links:
                for result_link in soup.find_all('a', class_='result__a'):
                    href = result_link.get('href')
                    if href and href.startswith('//duckduckgo.com/l/?'):
                        # Extract uddg parameter
                        import urllib.parse
                        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                        if 'uddg' in query_params:
                            links.append(query_params['uddg'][0])
            
            print(f"DEBUG: Total links found: {len(links)}")
            return links[:15]  # Limit to 15 results
        else:
            print(f"DEBUG: Non-200 response: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error searching DuckDuckGo: {e}")
        import traceback
        traceback.print_exc()
        return []


def search_demo(query):
    """
    Demo mode that returns sample results
    Use this to test the interface while you set up a real search API
    """
    # Sample results based on common queries
    sample_results = {
        "python": [
            "https://www.python.org/",
            "https://docs.python.org/3/tutorial/",
            "https://realpython.com/",
            "https://www.learnpython.org/",
            "https://www.programiz.com/python-programming",
            "https://www.w3schools.com/python/",
            "https://www.geeksforgeeks.org/python-programming-language/",
            "https://github.com/TheAlgorithms/Python",
            "https://www.codecademy.com/learn/learn-python-3",
            "https://python.land/python-tutorial"
        ],
        "web scraping": [
            "https://www.scrapingbee.com/blog/web-scraping-101-with-python/",
            "https://realpython.com/beautiful-soup-web-scraper-python/",
            "https://scrapy.org/",
            "https://www.zenrows.com/blog/web-scraping-python",
            "https://www.datacamp.com/tutorial/web-scraping-using-python",
            "https://github.com/scrapy/scrapy",
            "https://www.crummy.com/software/BeautifulSoup/bs4/doc/",
            "https://selenium-python.readthedocs.io/"
        ],
        "flask": [
            "https://flask.palletsprojects.com/",
            "https://flask.palletsprojects.com/en/3.0.x/quickstart/",
            "https://www.fullstackpython.com/flask.html",
            "https://github.com/pallets/flask",
            "https://realpython.com/tutorials/flask/",
            "https://flask.palletsprojects.com/en/3.0.x/tutorial/",
            "https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3"
        ]
    }
    
    # Find matching results based on query keywords
    query_lower = query.lower()
    results = []
    
    for keyword, urls in sample_results.items():
        if keyword in query_lower:
            results.extend(urls)
            break
    
    # If no specific match, return a default set
    if not results:
        results = [
            f"https://example.com/result1?q={query}",
            f"https://example.com/result2?q={query}",
            f"https://example.com/result3?q={query}",
            "https://en.wikipedia.org/wiki/" + query.replace(" ", "_"),
            "https://github.com/search?q=" + query.replace(" ", "+"),
            "https://stackoverflow.com/search?q=" + query.replace(" ", "+"),
        ]
    
    print(f"DEBUG: Demo mode returning {len(results)} results for '{query}'")
    return results


def search_google(query):
    """
    Main search function - currently uses demo mode
    
    To enable real searching:
    1. Use Google Custom Search API (recommended)
    2. Use Bing Search API
    3. Use SerpAPI or similar service
    
    Replace this function's content with API calls once you have credentials.
    """
    return search_demo(query)


def create_csv_from_links(links):
    """
    Create a CSV file from list of links and return as BytesIO object
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['URL'])  # Header
    for link in links:
        writer.writerow([link])
    
    # Convert to BytesIO for file download
    output.seek(0)
    return io.BytesIO(output.getvalue().encode('utf-8'))


@app.route('/')
def index():
    """
    Home page with search form
    """
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    """
    Handle search request and return results as JSON
    """
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Please enter a search query'}), 400
    
    # Perform search
    links = search_google(query)
    
    if not links:
        return jsonify({
            'query': query,
            'results': [],
            'message': 'No results found or unable to fetch results'
        })
    
    return jsonify({
        'query': query,
        'results': links,
        'count': len(links)
    })


@app.route('/download', methods=['POST'])
def download():
    """
    Download search results as CSV
    """
    data = request.get_json()
    links = data.get('links', [])
    query = data.get('query', 'search')
    
    if not links:
        return jsonify({'error': 'No links to download'}), 400
    
    # Create CSV
    csv_file = create_csv_from_links(links)
    
    return send_file(
        csv_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'spider_results_{query.replace(" ", "_")}.csv'
    )


@app.route('/health')
def health():
    """
    Health check endpoint
    """
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    # Run in debug mode for development
    # Set debug=False for production
    app.run(debug=True, host='0.0.0.0', port=8000)

