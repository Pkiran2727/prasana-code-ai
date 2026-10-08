import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
url = "https://html.duckduckgo.com/html/"
data = urllib.parse.urlencode({'q': 'news'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
try:
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', class_='result__url', limit=5):
        print(a.get('href'))
except Exception as e:
    print(e)
