import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ChronogolfClient:
    """
    A reverse-engineered client using session cookies to get real data.
    """
    
    def __init__(self):
        self.url = os.getenv("CHRONOGOLF_URL")
        self.cookie = os.getenv("CHRONOGOLF_COOKIE")
        self.referer = os.getenv("CHRONOGOLF_REFERER")
        
        # We must mimic the browser headers exactly
        self.headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "cookie": self.cookie,
            "referer": self.referer,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "sec-fetch-site": "same-origin"
        }

    def fetch_real_data(self):
        """
        Executes the GET request to fetch live tee times.
        """
        try:
            print(f"Connecting to Chrono Golf for Rondebosch Golf Club...")
            response = requests.get(self.url, headers=self.headers)
            
            # Check for success
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error: Could not fetch data. {e}")
            return None

if __name__ == "__main__":
    client = ChronogolfClient()
    data = client.fetch_real_data()
    
    if data:
        print("✅ Success! We have live data.")
        # This tells us how the data is organized
        if isinstance(data, dict):
            print(f"Top-level keys: {list(data.keys())}")
        elif isinstance(data, list):
            print(f"Data is a list with {len(data)} items.")
            if len(data) > 0:
                print(f"Sample item keys: {list(data[0].keys())}")