# Phase 1: Basic Building Design Web App
# File: app.py

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd
from datetime import datetime
import json
import sqlite3

app = Flask(__name__)
CORS(app)


class BuildingDesignService:
    def __init__(self):
        self.setup_database()
        self.load_climate_zones()
        self.load_building_standards()

    def setup_database(self):
        """Initialize database for storing designs and analysis results"""
        conn = sqlite3.connect('building_designs.db')
        cursor = conn.cursor()

        # Climate data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS climate_data (
                id INTEGER PRIMARY KEY,
                lat REAL,
                lng REAL,
                climate_zone TEXT,
                hdd INTEGER,  -- Heating Degree Days
                cdd INTEGER,  -- Cooling Degree Days
                solar_irradiance REAL,
                wind_speed REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Building designs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS building_designs (
                id INTEGER PRIMARY KEY,
                lat REAL,
                lng REAL,
                building_type TEXT,
                orientation REAL,
                window_wall_ratio REAL,
                energy_consumption REAL,
                design_parameters TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def load_climate_zones(self):
        """Load climate zone classifications"""
        self.climate_zones = {
            'very_hot': {'temp_range': (25, 45), 'strategy': 'minimize_solar_gain'},
            'hot': {'temp_range': (20, 30), 'strategy': 'moderate_solar_control'},
            'temperate': {'temp_range': (10, 25), 'strategy': 'balanced_design'},
            'cold': {'temp_range': (-5, 15), 'strategy': 'maximize_solar_gain'},
            'very_cold': {'temp_range': (-20, 5), 'strategy': 'maximum_insulation'}
        }

    def load_building_standards(self):
        """Load building standards and optimal parameters"""
        self.building_standards = {
            'residential': {
                'typical_wwr': 0.3,  # Window-to-Wall Ratio
                'optimal_orientation': 180,  # South-facing
                'thermal_mass': 'medium'
            },
            'office': {
                'typical_wwr': 0.4,
                'optimal_orientation': 165,  # Slightly south-east
                'thermal_mass': 'high'
            },
            'retail': {
                'typical_wwr': 0.2,
                'optimal_orientation': 90,  # East-facing
                'thermal_mass': 'low'
            }
        }

    def analyze_climate(self, lat, lng):
        """Analyze climate conditions for the given location"""
        # Simplified climate analysis based on latitude
        # In real implementation, use weather APIs

        avg_temp = 20 - abs(lat) * 0.5  # Rough temperature estimation

        # Determine climate zone
        climate_zone = 'temperate'
        for zone, data in self.climate_zones.items():
            temp_min, temp_max = data['temp_range']
            if temp_min <= avg_temp <= temp_max:
                climate_zone = zone
                break

        # Calculate solar potential
        solar_potential = max(0, 100 - abs(lat))  # Higher near equator

        # Estimate heating/cooling degree days
        hdd = max(0, (18 - avg_temp) * 365) if avg_temp < 18 else 0
        cdd = max(0, (avg_temp - 24) * 365) if avg_temp > 24 else 0

        return {
            'climate_zone': climate_zone,
            'avg_temperature': round(avg_temp, 1),
            'solar_potential': round(solar_potential, 1),
            'heating_degree_days': int(hdd),
            'cooling_degree_days': int(cdd),
            'strategy': self.climate_zones[climate_zone]['strategy']
        }

    def optimize_building_design(self, lat, lng, building_type='residential'):
        """Generate optimized building design parameters"""
        climate_data = self.analyze_climate(lat, lng)
        base_standards = self.building_standards.get(building_type, self.building_standards['residential'])

        # Optimize based on climate strategy
        strategy = climate_data['strategy']
        optimized_design = base_standards.copy()

        if strategy == 'minimize_solar_gain':
            # Hot climate optimization
            optimized_design.update({
                'window_wall_ratio': base_standards['typical_wwr'] * 0.7,  # Reduce windows
                'optimal_orientation': 0,  # North-facing to minimize solar gain
                'shading_required': True,
                'insulation_priority': 'roof',
                'ventilation_strategy': 'natural_cooling'
            })

        elif strategy == 'maximize_solar_gain':
            # Cold climate optimization
            optimized_design.update({
                'window_wall_ratio': base_standards['typical_wwr'] * 1.3,  # Increase windows
                'optimal_orientation': 180,  # South-facing for maximum solar gain
                'shading_required': False,
                'insulation_priority': 'walls',
                'ventilation_strategy': 'heat_recovery'
            })

        elif strategy == 'balanced_design':
            # Temperate climate optimization
            optimized_design.update({
                'window_wall_ratio': base_standards['typical_wwr'],
                'optimal_orientation': 165,  # Slightly south-east
                'shading_required': 'seasonal',
                'insulation_priority': 'balanced',
                'ventilation_strategy': 'mixed_mode'
            })

        # Calculate estimated energy performance
        energy_performance = self.estimate_energy_consumption(climate_data, optimized_design)

        return {
            'climate_analysis': climate_data,
            'optimized_parameters': optimized_design,
            'energy_performance': energy_performance,
            'recommendations': self.generate_recommendations(climate_data, optimized_design)
        }

    def estimate_energy_consumption(self, climate_data, design_params):
        """Simplified energy consumption estimation"""
        base_consumption = 100  # kWh/m²/year baseline

        # Adjust for climate
        if climate_data['heating_degree_days'] > 2000:
            heating_load = climate_data['heating_degree_days'] * 0.05
        else:
            heating_load = 0

        if climate_data['cooling_degree_days'] > 500:
            cooling_load = climate_data['cooling_degree_days'] * 0.08
        else:
            cooling_load = 0

        # Adjust for window-to-wall ratio
        wwr_impact = (design_params['window_wall_ratio'] - 0.3) * 50

        total_consumption = base_consumption + heating_load + cooling_load + wwr_impact

        return {
            'total_annual': round(max(20, total_consumption), 1),
            'heating_load': round(heating_load, 1),
            'cooling_load': round(cooling_load, 1),
            'lighting_load': 25,  # Assumed constant
            'equipment_load': 30  # Assumed constant
        }

    def generate_recommendations(self, climate_data, design_params):
        """Generate design recommendations"""
        recommendations = []

        # Climate-specific recommendations
        if climate_data['climate_zone'] == 'very_hot':
            recommendations.extend([
                "Use light-colored exterior materials to reflect heat",
                "Install horizontal shading devices on south-facing windows",
                "Consider double-height spaces for natural ventilation",
                "Use thermal mass for night cooling"
            ])
        elif climate_data['climate_zone'] == 'cold':
            recommendations.extend([
                "Maximize south-facing glazing for passive solar heating",
                "Use high-performance insulation (R-value > 30)",
                "Consider thermal mass to store solar heat",
                "Install triple-glazed windows"
            ])

        # Window-to-wall ratio recommendations
        wwr = design_params['window_wall_ratio']
        if wwr > 0.4:
            recommendations.append(f"High window ratio ({wwr:.1%}) may increase energy consumption")
        elif wwr < 0.2:
            recommendations.append(f"Low window ratio ({wwr:.1%}) may require more artificial lighting")

        return recommendations


# Initialize service
building_service = BuildingDesignService()


@app.route('/')
def home():
    return render_template('building_optimizer.html')


@app.route('/api/analyze-site')
def analyze_site():
    """API endpoint for site analysis"""
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        building_type = request.args.get('building_type', 'residential')

        analysis_result = building_service.optimize_building_design(lat, lng, building_type)

        return jsonify({
            'success': True,
            'data': analysis_result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/climate-data')
def get_climate_data():
    """API endpoint for climate data"""
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))

        climate_data = building_service.analyze_climate(lat, lng)

        return jsonify({
            'success': True,
            'data': climate_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


if __name__ == '__main__':
    print("Starting Building Design Optimizer...")
    print("Access at: http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)

