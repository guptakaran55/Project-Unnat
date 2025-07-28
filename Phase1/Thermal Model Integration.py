from pyEplus import PyEplus
import CoolProp.CoolProp as CP


class BuildingPhysicsEngine:
    def __init__(self):
        self.energyplus = PyEplus()
        self.setup_base_models()

    def create_building_model(self, params):
        """Create EnergyPlus building model"""
        building_dict = {
            'Building': {
                'Name': 'OptimizedBuilding',
                'North_Axis': params['orientation'],
                'Terrain': 'Urban',
                'Solar_Distribution': 'FullExteriorWithReflections'
            },
            'Zone': {
                'Name': 'ThermalZone1',
                'Volume': params['volume'],
                'Floor_Area': params['floor_area']
            },
            'BuildingSurface:Detailed': self.create_surfaces(params),
            'Window': self.create_windows(params),
            'Material': self.create_materials(params),
            'Construction': self.create_constructions(params)
        }

        return building_dict

    def simulate_energy_performance(self, building_model, weather_data):
        """Run EnergyPlus simulation"""
        results = self.energyplus.run_simulation(building_model, weather_data)

        return {
            'annual_heating': results['Heating:Electricity'],
            'annual_cooling': results['Cooling:Electricity'],
            'peak_heating_load': results['Peak_Heating_Load'],
            'peak_cooling_load': results['Peak_Cooling_Load'],
            'thermal_comfort': self.analyze_thermal_comfort(results)
        }

    def calculate_thermal_mass_effect(self, materials, climate_data):
        """Calculate thermal mass impact on energy performance"""
        thermal_mass_capacity = sum([
            mat['density'] * mat['specific_heat'] * mat['thickness']
            for mat in materials
        ])

        # Simplified thermal mass benefit calculation
        diurnal_temp_range = np.std(climate_data['hourly_temperature'][:24])
        mass_benefit = min(0.15, thermal_mass_capacity / 1000 * diurnal_temp_range / 10)

        return mass_benefit