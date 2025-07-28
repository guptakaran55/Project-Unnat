def parse_epw_file(self, lat, lng):
    """Parse EnergyPlus Weather file for detailed hourly data"""
    # Download EPW file for location
    epw_url = self.find_nearest_epw(lat, lng)

    if epw_url:
        epw_data = self.download_and_parse_epw(epw_url)
        return self.process_8760_data(epw_data)

    return None


def process_8760_data(self, epw_data):
    """Process 8760 hourly weather data"""
    return {
        'temperature': epw_data['dry_bulb_temperature'],
        'humidity': epw_data['relative_humidity'],
        'solar_irradiance': epw_data['global_horizontal_radiation'],
        'wind_speed': epw_data['wind_speed'],
        'wind_direction': epw_data['wind_direction']
    }