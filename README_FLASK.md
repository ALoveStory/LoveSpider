# 🕷️ Spider Search Engine - Flask Web Application

A web-based search crawler that extracts links from Google search results and provides downloadable CSV exports.

**Author:** Antwan Love (ADLJR)

## 📋 Features

- 🔍 Web-based search interface
- 🕸️ Link extraction and display
- 📊 Results displayed in a clean, modern UI
- 📥 Download results as CSV file
- 📱 Responsive design for mobile and desktop
- ⚡ Real-time search with loading indicators
- 🎮 **Demo Mode** - Test interface with sample results
- 🔌 **API-Ready** - Easy integration with Google/Bing/SerpAPI

## ⚡ Current Status: Demo Mode

The app currently runs in **demo mode** with sample results because Google and DuckDuckGo block automated scraping. See `API_INTEGRATION_GUIDE.md` for instructions on integrating real search APIs.

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/alovedev/Workspace/LoveSpider
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask development server:**
   ```bash
   python app.py
   ```

2. **Open your web browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Enter a search query and click "Search"** to see results!

## 📁 Project Structure

```
LoveSpider/
├── app.py                  # Flask application and API routes
├── spiderman.py            # Original CLI script (preserved)
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main web interface
├── static/
│   └── css/
│       └── style.css      # Styling and animations
└── README_FLASK.md        # This file
```

## 🎯 Usage

### Web Interface

1. Enter your search query in the input field
2. Click the "Search" button
3. View results in the list below
4. Click "Download CSV" to export results

### API Endpoints

The application also provides REST API endpoints:

#### Search
```http
POST /search
Content-Type: application/json

{
  "query": "your search query"
}
```

**Response:**
```json
{
  "query": "your search query",
  "results": ["url1", "url2", "..."],
  "count": 10
}
```

#### Download CSV
```http
POST /download
Content-Type: application/json

{
  "query": "search query",
  "links": ["url1", "url2", "..."]
}
```

#### Health Check
```http
GET /health
```

## ⚙️ Configuration

### Change Port or Host

Edit `app.py` and modify the last line:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Production Deployment

For production, set `debug=False` and use a production WSGI server like **Gunicorn**:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🚀 Deployment Options

### Option 1: Heroku

1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku master
   ```

### Option 2: Render

1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`

### Option 3: PythonAnywhere

1. Upload files to PythonAnywhere
2. Create a new web app
3. Configure WSGI file to point to your app
4. Install dependencies in the virtual environment

### Option 4: DigitalOcean App Platform

1. Connect your repository
2. Select Python as the environment
3. Auto-detects requirements.txt
4. Configure run command: `gunicorn app:app`

## ⚠️ Important Notes

### Legal Considerations

**WARNING:** Web scraping Google may violate their Terms of Service. For production use, consider:

- **Google Custom Search API** - 100 free queries/day
- **SerpAPI** - Paid service for search results
- **Bing Search API** - Alternative with free tier
- **DuckDuckGo API** - Free alternative

### Rate Limiting

The current implementation doesn't include rate limiting. For production:

1. Install Flask-Limiter:
   ```bash
   pip install Flask-Limiter
   ```

2. Add to `app.py`:
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(
       app=app,
       key_func=lambda: request.remote_addr,
       default_limits=["100 per day", "10 per minute"]
   )
   ```

### Security Enhancements

For production deployment:

1. Change the secret key in `app.py`
2. Add input validation and sanitization
3. Implement CAPTCHA (e.g., reCAPTCHA)
4. Add HTTPS/SSL certificates
5. Set up CORS properly if building a separate frontend

## 🐛 Troubleshooting

### Port already in use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Module not found errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# Then reinstall
pip install -r requirements.txt
```

### No results returned
- Google may be blocking requests (use a VPN or official API)
- Check your internet connection
- Review console logs for error messages

## 📝 Development

### Run in Debug Mode

Debug mode is enabled by default in `app.py`. This provides:
- Auto-reload on code changes
- Detailed error pages
- Debug toolbar

### Adding Features

Some ideas for enhancement:
- User authentication
- Search history tracking
- Database integration (PostgreSQL/MongoDB)
- Advanced filtering options
- Multiple search engine support
- Scheduled/recurring searches
- API key authentication

## 📄 License

This project is created for educational purposes. Please respect website terms of service and robots.txt when scraping.

## 👤 Author

**Antwan Love (ADLJR)**

## 🙏 Acknowledgments

- Flask documentation
- BeautifulSoup documentation
- Web scraping best practices community

---

**Enjoy your Spider Search Engine!** 🕷️🕸️

