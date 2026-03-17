import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class PostmortemScraper:
    def __init__(self):
        # We can add headers or user agents here
        self.headers = {"User-Agent": "Mozilla/5.0"}
    
    def scrape_url(self, url: str) -> Dict[str, str]:
        """Scrape text from a single URL and return title and raw text."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            title = soup.title.string if soup.title else "Unknown Title"
            
            # Extract main content, avoiding nav/scripts
            for script in soup(["script", "style", "nav", "footer"]):
                script.extract()
            
            text = soup.get_text(separator=" ", strip=True)
            return {"url": url, "title": title, "text": text}
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return {"url": url, "title": "Error", "text": ""}
