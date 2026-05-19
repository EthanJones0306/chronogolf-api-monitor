# ChronoGolf API Monitor

A Python automation tool that monitors **Chrono Golf's private API** for available tee times and enables automated booking at Rondebosch Golf Club.

## Project Overview

This is a reverse-engineered API client that demonstrates:
- **API reverse-engineering** through browser network inspection
- **Session-based authentication** using cookies and CSRF tokens
- **Continuous monitoring** with configurable polling intervals
- **Automated booking workflow** with three-step reservation process

The tool periodically checks for available golf tee times matching your criteria (price, time, hole count) and can automatically lock and book slots.

## Features

✅ Poll for available tee times at specified intervals  
✅ Filter by price, start time, and hole count  
✅ Freeze tee times (add to cart)  
✅ Automatically book confirmed reservations  
✅ Error handling and request retry logic  
✅ Browser-mimicking headers to avoid detection  

## Setup

### Prerequisites
- Python 3.8+
- Active Chrono Golf account with valid session

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your authentication credentials:
   ```
   CHRONOGOLF_COOKIE=your_session_cookie_here
   CHRONOGOLF_REFERER=https://www.chronogolf.com/marketplace
   CHRONOGOLF_CSRF_TOKEN=your_csrf_token_here
   ```

### Getting Your Credentials

1. Open Chrono Golf in your browser and log in
2. Open Developer Tools → Network tab
3. Make any request (e.g., search for tee times)
4. Copy the `Cookie` header → paste into `CHRONOGOLF_COOKIE`
5. Copy the `X-CSRF-Token` header → paste into `CHRONOGOLF_CSRF_TOKEN`
6. Copy the `Referer` header → paste into `CHRONOGOLF_REFERER`

## Usage

### Monitor for Tee Times
```bash
python main.py
```
Continuously checks for available slots matching your criteria every 5 minutes.

### Test the Full Booking Flow
```bash
python chronogolf_client.py
```
Fetches data, freezes a slot, and books it (edit `test_date` variable to change the date).

## Architecture

### `chronogolf_client.py`
Core API client with three main methods:
- `fetch_real_data(date)` — Query available tee times for a given date
- `freeze_tee_time(id)` — Lock a tee time in your cart
- `book_tee_time(id)` — Confirm and complete the reservation

### `parser.py`
Extracts and structures API response data into clean slot objects with:
- Start time
- Holes available
- Price per person
- Max players
- UUID and hole number

### `main.py`
Monitoring loop that:
1. Fetches tee times every 5 minutes
2. Filters for your criteria (R500 max, before 9am)
3. Alerts when matches found
4. Ready to trigger booking notifications

## Configuration

Current criteria (hardcoded in `main.py`):
- **Max price**: R500 per person
- **Latest time**: 9:00 AM
- **Polling interval**: 5 minutes
- **Course**: Rondebosch Golf Club

## Security Notes

⚠️ **Do not commit `.env` files** — credentials are sensitive  
⚠️ **Respect rate limits** — the 5-minute interval helps avoid IP bans  
⚠️ **Use responsibly** — this is for personal use only  

## What I Learned

- Reverse-engineering undocumented APIs through browser inspection
- Managing stateful API interactions (freeze → confirm workflow)
- Session-based authentication patterns
- Mimicking browser behavior to avoid bot detection
- Building resilient monitoring loops

## Future Improvements

- [ ] Move hardcoded values to config file
- [ ] Add logging instead of print statements
- [ ] Implement notification system (email/SMS alerts)
- [ ] Add unit tests with mocked API responses
- [ ] Support multiple courses and criteria
- [ ] Database to track historical availability
- [ ] Web UI dashboard

## License

Personal project — for learning purposes only.