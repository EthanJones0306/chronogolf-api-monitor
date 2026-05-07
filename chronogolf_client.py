import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ChronogolfClient:
    def __init__(self):
        self.cookie = os.getenv("CHRONOGOLF_COOKIE")
        self.referer = os.getenv("CHRONOGOLF_REFERER")
        
        # We define the base URL WITHOUT the date part
        # Note: I removed the start_date from this string
        self.base_url = "https://www.chronogolf.com/marketplace/v2/teetimes"
        
        self.headers = {
            "accept": "application/json",
            "cookie": self.cookie,
            "referer": self.referer,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        }

    def fetch_real_data(self, target_date):
        """
        Fetches tee times for a specific date (YYYY-MM-DD).
        """
        # We broaden the search window to start at 6:00 AM
        params = {
            "start_date": target_date,
            "course_ids": "ee003157-9a13-4876-97bf-58435c7f7d8e",
            "holes": "9,18",
            "start_time": "06:00", # Changed from 16:20
            "page": "1"
        }
        
        try:
            print(f"Checking Chrono Golf for date: {target_date}...")
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    client = ChronogolfClient()
    
    # Check Sunday
    target = "2026-05-20" 
    data = client.fetch_real_data(target)
    
    print("\n--- Diagnostic Report ---")
    
    if data is None:
        print("❌ The API returned nothing at all (None). Check your connection.")
    elif isinstance(data, dict):
        print(f"✅ Received a Dictionary. Keys: {list(data.keys())}")
        
        # Check the 'teetimes' key specifically
        teetimes = data.get('teetimes')
        if teetimes is not None:
            print(f"📊 'teetimes' type: {type(teetimes)}")
            print(f"🔢 'teetimes' length: {len(teetimes)}")
            
            if len(teetimes) > 0:
                print("📝 Sample of first tee time:")
                import json
                print(json.dumps(teetimes[0], indent=2))
            else:
                print("❓ The 'teetimes' list is empty. This is suspicious.")
        else:
            print("⚠️ The key 'teetimes' was not found in the response.")
    else:
        print(f"🤔 Received unexpected data type: {type(data)}")