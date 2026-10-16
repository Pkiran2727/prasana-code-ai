import logging
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import requests

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
                real_url = href
                if "uddg=" in href:
                    real_url = urllib.parse.unquote(href.split("uddg=")[1].split("&")[0])
                    
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

def execute_search_wikipedia(query: str) -> Dict[str, Any]:
    """Fetch Wikipedia summary via Wikipedia REST API (standard python requests, no third-party package needed)."""
    logger.info(f"Searching Wikipedia for {query}")
    try:
        encoded_query = urllib.parse.quote(query)
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"
        headers = {'User-Agent': 'PrasanaCodeAI/1.0 (educational coding tutor)'}
        res = requests.get(api_url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return {
                "status": "success",
                "title": data.get("title", query),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                "summary": data.get("extract", "")
            }
        return {"status": "error", "message": f"Wikipedia article not found for {query}"}
    except Exception as e:
        logger.error(f"Wikipedia search failed: {e}")
        return {"status": "error", "message": str(e)}
