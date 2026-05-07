class TeeTimeParser:
    @staticmethod
    def parse(raw_data):
        """
        Takes the raw JSON and returns a clean list of available times.
        """
        results = []
        teetimes = raw_data.get('teetimes', [])
        
        for slot in teetimes:
            # Extracting the nested data safely
            price_info = slot.get('default_price', {})
            course_info = slot.get('course', {})

            bookable_holes = course_info.get('bookable_holes')
            max_holes = max(bookable_holes) if bookable_holes else None
            
            clean_slot = {
                "time": slot.get('start_time'),
                "holes_available": max_holes,
                "price": price_info.get('subtotal'),
                "max_players": slot.get('max_player_size'),
                "uuid": slot.get('uuid'),
                "hole": slot.get('hole'),
                "players": slot.get('max_player_size'),
            
            }
            results.append(clean_slot)
            
        return results