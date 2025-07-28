import rhinoinside

rhinoinside.load()
import Rhino.Geometry as rg
from compas.geometry import Box, Plane, Point, Vector


class ParametricBuildingGenerator:
    def __init__(self):
        self.building_templates = self.load_building_templates()

    def generate_building_variants(self, site_params, design_constraints):
        """Generate multiple building design variants"""
        variants = []

        # Base building parameters
        base_params = {
            'length': [20, 30, 40],
            'width': [15, 20, 25],
            'height': [3, 6, 9, 12],
            'orientation': range(0, 360, 15),
            'window_wall_ratio': np.arange(0.1, 0.6, 0.1)
        }

        # Generate combinations
        for length in base_params['length']:
            for width in base_params['width']:
                for height in base_params['height']:
                    for orientation in base_params['orientation']:
                        for wwr in base_params['window_wall_ratio']:
                            if self.meets_constraints(length, width, height, site_params):
                                variant = self.create_building_geometry({
                                    'length': length,
                                    'width': width,
                                    'height': height,
                                    'orientation': orientation,
                                    'wwr': wwr
                                })
                                variants.append(variant)

        return variants[:100]  # Limit to top 100 variants

    def create_building_geometry(self, params):
        """Create 3D building geometry"""
        # Base building footprint
        footprint = rg.Rectangle3d(
            rg.Plane.WorldXY,
            params['length'],
            params['width']
        )

        # Extrude to create building mass
        building_mass = rg.Extrusion.Create(
            footprint.ToNurbsCurve(),
            params['height'],
            True
        )

        # Apply rotation for orientation
        rotation = rg.Transform.Rotation(
            math.radians(params['orientation']),
            rg.Vector3d.ZAxis,
            rg.Point3d.Origin
        )
        building_mass.Transform(rotation)

        # Add windows
        facades = self.extract_facades(building_mass)
        windows = self.create_windows(facades, params['wwr'])

        return {
            'geometry': building_mass,
            'windows': windows,
            'parameters': params,
            'area': params['length'] * params['width'],
            'volume': params['length'] * params['width'] * params['height']
        }

    def create_windows(self, facades, wwr):
        """Create windows on building facades"""
        windows = []

        for facade in facades:
            facade_area = self.calculate_surface_area(facade)
            window_area = facade_area * wwr

            # Create window grid
            window_grid = self.create_window_grid(facade, window_area)
            windows.extend(window_grid)

        return windows