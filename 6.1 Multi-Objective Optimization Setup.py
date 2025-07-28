from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
import numpy as np


class BuildingOptimizationProblem(Problem):
    """Multi-objective optimization problem for building design"""

    def __init__(self, climate_data, site_constraints):
        self.climate_data = climate_data
        self.site_constraints = site_constraints

        super().__init__(
            n_var=5,  # orientation, wwr, height, length, width
            n_obj=3,  # energy, cost, comfort
            n_constr=2,  # site constraints
            xl=np.array([0, 0.1, 3, 10, 10]),
            xu=np.array([360, 0.8, 20, 50, 50])
        )

    def _evaluate(self, X, out, *args, **kwargs):
        # Initialize arrays for objectives and constraints
        f1 = np.zeros(X.shape[0])  # Energy consumption (minimize)
        f2 = np.zeros(X.shape[0])  # Cost (minimize)
        f3 = np.zeros(X.shape[0])  # Comfort (maximize, so negate)

        g1 = np.zeros(X.shape[0])  # Site area constraint
        g2 = np.zeros(X.shape[0])  # Zoning height constraint

        for i, design in enumerate(X):
            # Extract design parameters
            orientation, wwr, height, length, width = design

            # Calculate objectives
            energy = self.calculate_energy_consumption(design)
            cost = self.calculate_construction_cost(design)
            comfort = self.calculate_thermal_comfort(design)

            # Calculate constraints
            site_area_used = length * width
            max_site_area = self.site_constraints['max_area']
            max_height = self.site_constraints['max_height']

            f1[i] = energy
            f2[i] = cost
            f3[i] = -comfort  # Negate for maximization

            g1[i] = site_area_used - max_site_area
            g2[i] = height - max_height

        out["F"] = np.column_stack([f1, f2, f3])
        out["G"] = np.column_stack([g1, g2])


class MultiObjectiveOptimizer:
    def __init__(self, climate_data, site_constraints):
        self.problem = BuildingOptimizationProblem(climate_data, site_constraints)

    def optimize(self, population_size=100, generations=50):
        """Run multi-objective optimization"""
        algorithm = NSGA2(pop_size=population_size)

        result = minimize(
            self.problem,
            algorithm,
            ('n_gen', generations),
            verbose=True
        )

        return self.process_results(result)

    def process_results(self, result):
        """Process optimization results"""
        pareto_front = result.F
        pareto_designs = result.X

        # Find knee point (best compromise solution)
        knee_point = self.find_knee_point(pareto_front)
        best_design = pareto_designs[knee_point]

        return {
            'pareto_front': pareto_front,
            'pareto_designs': pareto_designs,
            'best_design': {
                'orientation': best_design[0],
                'window_wall_ratio': best_design[1],
                'height': best_design[2],
                'length': best_design[3],
                'width': best_design[4]
            },
            'performance': {
                'energy': pareto_front[knee_point, 0],
                'cost': pareto_front[knee_point, 1],
                'comfort': -pareto_front[knee_point, 2]
            }
        }