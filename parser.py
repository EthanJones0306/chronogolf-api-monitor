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
            
            clean_slot = {
                "time": slot.get('start_time'),
                "holes": price_info.get('bookable_holes'),
                "price": price_info.get('subtotal'),
                "max_players": slot.get('max_player_size'),
                "uuid": slot.get('uuid')
            }
            results.append(clean_slot)
            
        return results