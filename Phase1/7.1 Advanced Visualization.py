# 3D Building Visualization with Three.js integration
class ThreeJSVisualization:
    def __init__(self):
        self.scene_data = {}

    def create_3d_building_model(self, building_geometry):
        """Create Three.js compatible 3D building model"""
        vertices = []
        faces = []
        materials = []

        # Convert building geometry to Three.js format
        for surface in building_geometry['surfaces']:
            # Extract vertices and faces
            surface_vertices = surface['vertices']
            surface_faces = surface['faces']

            vertices.extend(surface_vertices)
            faces.extend(surface_faces)
            materials.append(surface['material'])

        return {
            'vertices': vertices,
            'faces': faces,
            'materials': materials,
            'metadata': {
                'area': building_geometry['area'],
                'volume': building_geometry['volume']
            }
        }

    def create_solar_analysis_visualization(self, solar_data):
        """Create solar analysis visualization"""
        return {
            'solar_vectors': solar_data['sun_vectors'],
            'shadow_geometry': solar_data['shadows'],
            'irradiance_map': solar_data['surface_irradiance']
        }