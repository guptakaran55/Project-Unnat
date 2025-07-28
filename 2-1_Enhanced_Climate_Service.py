# Add to app.py
from pvlib import solarposition, irradiance
from windpowerlib import ModelChain, WindTurbine
import psychrolib
import requests
import numpy as np


class AdvancedClimateService:
    def __init__(self):
        psychrolib.SetUnitSystem(psychrolib.SI)

    def get_solar_data(self, lat, lng, year=2023):
        """Calculate detailed solar radiation data"""
        # Solar position throughout the year
        times = pd.date_range(f'{year}-01-01', f'{year}-12-31', freq='D')
        solar_pos = solarposition.get_solarposition(times, lat, lng)

        # Clear sky radiation
        clearsky = clearsky.ineichen(times, lat, lng)

        return {
            'annual_irradiation': clearsky['ghi'].sum(),
            'peak_sun_hours': clearsky['ghi'].sum() / 1000,
            'seasonal_variation': self.calculate_seasonal_variation(clearsky['ghi'])
        }

    def get_wind_data(self, lat, lng):
        """Calculate wind energy potential"""
        # NASA POWER wind data
        wind_data = self.fetch_nasa_wind_data(lat, lng)

        return {
            'avg_wind_speed': wind_data['mean'],
            'wind_power_density': self.calculate_wind_power_density(wind_data),
            'prevailing_direction': wind_data['direction']
        }

    def calculate_comfort_indices(self, temp, humidity, wind_speed):
        """Calculate thermal comfort indices"""
        # Heat Index
        heat_index = psychrolib.GetHeatIndex(temp, humidity)

        # Wind Chill
        wind_chill = 13.12 + 0.6215 * temp - 11.37 * (wind_speed ** 0.16) + 0.3965 * temp * (wind_speed ** 0.16)

        return {
            'heat_index': heat_index,
            'wind_chill': wind_chill,
            'comfort_category': self.categorize_comfort(heat_index, wind_chill)
        }


2