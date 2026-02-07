import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import certifi
import os
import re

class TheaterScraper:
    # Using the dedicated ticketing system URL
    BASE_URL = "https://bilety.teatr-rzeszow.pl/MSI/mvc/pl"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        # Support bypassing SSL verification if needed
        self.verify_ssl = os.getenv("VERIFY_SSL", "true").lower() == "true"
        if self.verify_ssl:
            self.session.verify = certifi.where()
        else:
            self.session.verify = False
            # Suppress insecure request warnings if user explicitly disabled verification
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_upcoming_plays(self):
        """Fetches the ticketing page and extracts upcoming plays."""
        try:
            response = self.session.get(self.BASE_URL)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {self.BASE_URL}: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        plays_dict = {}
        
        # Iterate over large-screen list items to avoid duplicates from hidden mobile blocks
        for row in soup.select("div.list-group-item.visible-lg"):
            title_tag = row.select_one(".event-title")
            if not title_tag:
                continue
                
            title = title_tag.get_text(strip=True)
            
            # Extract description
            desc_container = row.select_one(".media-body")
            description = ""
            if desc_container:
                # Remove the title text from the body text to get the description
                full_body_text = desc_container.get_text(" ", strip=True)
                description = full_body_text.replace(title, "").replace("Opis", "").strip()
                description = re.sub(r'^[\s,.:;]+', '', description)
            
            # Extract dates from the purple badges
            dates = []
            for badge in row.select(".badge-purple"):
                # Badge contains visible date + hidden sr-only text
                # We want just the date/time part (first 12 chars usually "DD MMM HH:MM")
                date_text = badge.contents[0].strip() if badge.contents else ""
                if date_text:
                    dates.append(date_text)
            
            date_str = ", ".join(sorted(list(set(dates))))
            
            desc_link = row.select_one("a.badge-cart")
            details_url = urljoin(self.BASE_URL, desc_link['href']) if desc_link else self.BASE_URL

            # Key by title to merge any variations, though visible-lg should handle it
            if title not in plays_dict:
                plays_dict[title] = {
                    "title": title,
                    "date": date_str,
                    "url": details_url,
                    "description": description[:500] + ("..." if len(description) > 500 else "")
                }
            else:
                # If we found more dates for the same title, add them
                existing_dates = set(plays_dict[title]["date"].split(", "))
                existing_dates.update(dates)
                plays_dict[title]["date"] = ", ".join(sorted(list(existing_dates)))

        return list(plays_dict.values())

    def get_play_description(self, url):
        return "Description already retrieved during list scraping."