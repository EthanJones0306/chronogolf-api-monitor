import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ChronogolfClient:
    """
    A reverse-engineered client using session cookies to interact with Chrono Golf's private API.
    """
    
    def __init__(self):
        self.cookie = os.getenv("CHRONOGOLF_COOKIE")
        self.referer = os.getenv("CHRONOGOLF_REFERER")
        
        # Base URLs for the different endpoints we discovered
        self.market_url = "https://www.chronogolf.com/marketplace/v2/teetimes"
        self.freeze_base_url = "https://www.chronogolf.com/private_api/teetimes"
        self.reserve_url = "https://www.chronogolf.com/marketplace/reservations"
        self.csrf_token = os.getenv("CHRONOGOLF_CSRF_TOKEN") # <-- Load the new token
        
        # Our "Browser Mimic" headers
        self.headers = {
            "accept": "application/json",
            "cookie": self.cookie,
            "referer": self.referer,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Host": "www.chronogolf.com",
            "Content-Type": "application/json", # Crucial for the POST requests
            "x-csrf-token": self.csrf_token  # <-- Inject the token into the headers!
        }

    def fetch_real_data(self, target_date):
        """
        STEP 1: Fetches available tee times for a specific date (YYYY-MM-DD).
        """
        params = {
            "start_date": target_date,
            "course_ids": "ee003157-9a13-4876-97bf-58435c7f7d8e", # Rondebosch UUID
            "holes": "9,18",
            "start_time": "06:00", # Full day search
            "page": "1"
        }
        
        try:
            response = requests.get(self.market_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def freeze_tee_time(self, tee_time_id): 
        """
        STEP 2: Sends a POST request to lock a specific tee time slot in the cart.
        """
        freeze_url = f"{self.freeze_base_url}/{tee_time_id}/freeze" # Append the ID for the specific tee time to the URL to freeze it 
        
        try:
            # Empty JSON payload as discovered in the Network tab
            response = requests.post(freeze_url, headers=self.headers, json={})
            
            if response.status_code in [200, 201]:
                print(f"✅ Successfully froze tee time ID: {tee_time_id}")
                return response.json()
            else:
                print(f"❌ Failed to freeze. Status Code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error freezing tee time: {e}")
            return None

    def book_tee_time(self, teetime_id):
        """
        STEP 3: Sends the final POST request to confirm and book the tee time.
        """
        payload = {
            "reservation": {
                "club_id": 18534,
                "teetime_id": teetime_id,
                "holes": 18,
                "state": "confirmed",
                "source": "chronogolf",
                "medium": "dashboard",
                "rounds_attributes": [
                    {
                        "affiliation_type_id": 111447, # Your specific Member ID
                        "state": "reserved"
                    }
                ]
            }
        }
        
        try:
            response = requests.post(self.reserve_url, headers=self.headers, json=payload)
            
            if response.status_code == 201:
                print("🎉 SUCCESS! Tee time is officially booked!")
                return response.json()
            else:
                print(f"❌ Failed to confirm booking. Status Code: {response.status_code}")
                print(f"Server says: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error confirming booking: {e}")
            return None

# # Quick test block
# if __name__ == "__main__":
#     client = ChronogolfClient()
#     print("ChronoGolf Client is ready!")
#     # To test the full flow, you would chain them here:
#     # data = client.fetch_real_data("2026-05-15")
#     # ... parse data to find a teetime_id ...
#     # client.freeze_tee_time(teetime_id)
#     # client.book_tee_time(teetime_id)

if __name__ == "__main__":
    client = ChronogolfClient()
    
    # 1. Pick a date a few days from now that you know has openings
    test_date = "2026-05-18" # Change this if needed!
    print(f"--- Starting Live API Test for {test_date} ---")
    
    # STEP 1: Fetch the data
    data = client.fetch_real_data(test_date)
    
    if data and 'teetimes' in data and len(data['teetimes']) > 0:
        # Grab the very first available tee time in the list
        first_slot = data['teetimes'][0]
        test_id = first_slot.get('id')
        test_time = first_slot.get('start_time')
        
        print(f"🎯 Target Acquired: Slot at {test_time} (ID: {test_id})")
        
        # STEP 2: Freeze the slot (Safe to test - just goes to your cart)
        print("🧊 Attempting to freeze slot...")
        freeze_result = client.freeze_tee_time(test_id)
        
        if freeze_result:
            print("\n✅ FREEZE SUCCESSFUL! Open your browser and check your Chrono Golf cart right now.")
            
            # STEP 3: The Final Booking (DANGER ZONE ⚠️)
            # Remove the '#' from the two lines below ONLY if you actually want to book this slot!
            
            print("🚀 Firing final booking payload...")
            client.book_tee_time(test_id)
            
    else:
        print("❌ No tee times found for this date. Try changing 'test_date'.")