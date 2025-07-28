from radiance import RadianceScene


class DaylightingAnalysis:
    def __init__(self):
        self.radiance = RadianceScene()

    def calculate_daylight_autonomy(self, building_geometry, location):
        """Calculate daylight autonomy and useful daylight illuminance"""
        # Set up Radiance scene
        scene = self.radiance.create_scene(building_geometry)

        # Run annual daylight simulation
        illuminance_results = self.radiance.run_annual_simulation(
            scene, location['lat'], location['lng']
        )

        # Calculate metrics
        daylight_autonomy = self.calculate_DA(illuminance_results, threshold=300)
        useful_daylight_illuminance = self.calculate_UDI(illuminance_results)

        return {
            'daylight_autonomy': daylight_autonomy,
            'useful_daylight_illuminance': useful_daylight_illuminance,
            'annual_sunlight_exposure': self.calculate_ASE(illuminance_results)
        }

    def optimize_window_placement(self, facade_geometry, orientation):
        """Optimize window placement for daylighting"""
        # Generate window placement options
        window_options = self.generate_window_layouts(facade_geometry)

        best_layout = None
        best_score = 0

        for layout in window_options:
            da_score = self.calculate_daylight_performance(layout, orientation)
            if da_score > best_score:
                best_score = da_score
                best_layout = layout

        return best_layout, best_score