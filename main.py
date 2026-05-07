import time
from chronogolf_client import ChronogolfClient
from parser import TeeTimeParser

def run_monitor():
    client = ChronogolfClient()
    target_date = "2026-05-20"  # Change this to your desired date (YYYY-MM-DD)
    
    print(f"--- ChronoGolf Monitor Started for {target_date} ---")
    
    # Infinite loop to keep checking for new tee times
    while True:
        raw_data = client.fetch_real_data(target_date)
        
        if raw_data:
            available_slots = TeeTimeParser.parse(raw_data)
            
            if available_slots:
                print(f"Found {len(available_slots)} times! Checking for your favorite...")
                # Logic: Find a slot under R500 before 9:00 AM
                for slot in available_slots:
                    if slot['price'] <= 500:
                        print(f"🎯 MATCH FOUND: {slot['holes_available']} hole {slot['players']} ball at {slot['time']} for R{slot['price']} per person on hole {slot['hole']}")
                        # This is where we will trigger the notification next!
            else:
                print("No slots found yet. Keeping watch... 👀")
        
        # Wait 5 minutes before checking again to avoid being banned
        print("Waiting 5 minutes...")
        time.sleep(300) 

if __name__ == "__main__":
    run_monitor()