import logging
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import trafilatura
import requests
import yfinance as yf
import wikipedia
import datetime

logger = logging.getLogger(__name__)

def execute_search_web(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Perform a web search using DuckDuckGo HTML endpoint with BeautifulSoup.
    Returns a dictionary containing the search results.
    """
    logger.info(f"Searching web for: {query}")
    try:
        results = []
        url = "https://html.duckduckgo.com/html/"
        data = urllib.parse.urlencode({'q': query}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        for a in soup.find_all('a', class_='result__url', limit=max_results):
            href = a.get('href')
            if href:
                # Duckduckgo wraps urls in their redirector, extract the real url
                real_url = href
                if "uddg=" in href:
                    real_url = urllib.parse.unquote(href.split("uddg=")[1].split("&")[0])
                    
                # find the parent snippet
                parent = a.find_parent('div', class_='result')
                title = ""
                snippet = ""
                if parent:
                    title_elem = parent.find('h2', class_='result__title')
                    snippet_elem = parent.find('a', class_='result__snippet')
                    if title_elem:
                        title = title_elem.text.strip()
                    if snippet_elem:
                        snippet = snippet_elem.text.strip()
                        
                results.append({
                    "title": title,
                    "href": real_url,
                    "body": snippet
                })
                
        return {"status": "success", "results": results}
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return {"status": "error", "message": str(e)}

def execute_read_url(url: str) -> Dict[str, Any]:
    """
    Fetch and extract text content from a URL using Trafilatura.
    """
    logger.info(f"Reading URL: {url}")
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return {"status": "error", "message": "Failed to download URL content."}
        
        text = trafilatura.extract(downloaded)
        if not text:
            return {"status": "error", "message": "Failed to extract text from URL."}
            
        return {"status": "success", "text": text}
    except Exception as e:
        logger.error(f"Reading URL failed: {e}")
        return {"status": "error", "message": str(e)}

def execute_get_weather(location: str, mode: str = "current") -> Dict[str, Any]:
    """
    Fetch weather using Open-Meteo. Modes: 'current', 'forecast', 'historical'
    """
    logger.info(f"Fetching weather for {location} (mode: {mode})")
    try:
        # Geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(location)}&count=1&format=json"
        geo_res = requests.get(geo_url).json()
        if not geo_res.get("results"):
            return {"status": "error", "message": "Location not found"}
        
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        tz = geo_res["results"][0].get("timezone", "UTC")
        
        if mode == "current":
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone={tz}"
        elif mode == "forecast":
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone={tz}"
        elif mode == "historical":
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=7)
            url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone={tz}"
        else:
            return {"status": "error", "message": "Invalid mode. Use current, forecast, or historical"}
            
        res = requests.get(url).json()
        return {"status": "success", "data": res}
    except Exception as e:
        logger.error(f"Weather API failed: {e}")
        return {"status": "error", "message": str(e)}

def execute_get_stock(ticker: str) -> Dict[str, Any]:
    """Fetch stock info using yfinance."""
    logger.info(f"Fetching stock info for {ticker}")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "status": "success", 
            "data": {
                "price": info.get("currentPrice", info.get("regularMarketPrice")),
                "currency": info.get("currency"),
                "marketCap": info.get("marketCap"),
                "name": info.get("shortName"),
                "summary": info.get("longBusinessSummary", "")[:500] + "..."
            }
        }
    except Exception as e:
        logger.error(f"Stock API failed: {e}")
        return {"status": "error", "message": str(e)}

def execute_get_crypto(coin_id: str) -> Dict[str, Any]:
    """Fetch crypto price using CoinGecko."""
    logger.info(f"Fetching crypto price for {coin_id}")
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id.lower()}&vs_currencies=usd&include_market_cap=true&include_24hr_change=true"
        res = requests.get(url).json()
        if not res:
            return {"status": "error", "message": "Crypto not found. Use full name like 'bitcoin' or 'ethereum'"}
        return {"status": "success", "data": res}
    except Exception as e:
        logger.error(f"Crypto API failed: {e}")
        return {"status": "error", "message": str(e)}

def execute_search_wikipedia(query: str) -> Dict[str, Any]:
    """Fetch Wikipedia summary."""
    logger.info(f"Searching Wikipedia for {query}")
    try:
        summary = wikipedia.summary(query, sentences=3)
        page = wikipedia.page(query)
        return {
            "status": "success",
            "title": page.title,
            "url": page.url,
            "summary": summary
        }
    except wikipedia.exceptions.DisambiguationError as e:
        return {"status": "error", "message": f"Query is ambiguous. Options: {e.options[:5]}"}
    except wikipedia.exceptions.PageError:
        return {"status": "error", "message": "Wikipedia page not found."}
    except Exception as e:
        logger.error(f"Wikipedia API failed: {e}")
        return {"status": "error", "message": str(e)}
