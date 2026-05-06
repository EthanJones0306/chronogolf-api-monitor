import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ChronogolfClient:
    """
    A reverse-engineered client using session cookies to get real data.
    """
    
    def __init__(self): # Function to initialise the client with environment variables and headers
        # Initialise URL, cookie, and referer from environment variables
        self.url = os.getenv("CHRONOGOLF_URL")
        self.cookie = os.getenv("CHRONOGOLF_COOKIE")
        self.referer = os.getenv("CHRONOGOLF_REFERER")
        
        # Mimic browser headers to avoid being blocked by the server
        self.headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "cookie": self.cookie,
            "referer": self.referer,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "sec-fetch-site": "same-origin"
        }
