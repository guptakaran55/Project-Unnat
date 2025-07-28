import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env


class BuildingDesignEnv(gym.Env):
    """Gym environment for building design optimization"""

    def __init__(self, climate_data, site_constraints):
        super(BuildingDesignEnv, self).__init__()

        self.climate_data = climate_data
        self.site_constraints = site_constraints

        # Action space: [orientation, wwr, height, length, width]
        self.action_space = gym.spaces.Box(
            low=np.array([0, 0.1, 3, 10, 10]),
            high=np.array([360, 0.8, 20, 50, 50]),
            dtype=np.float32
        )

        # Observation space: climate and site parameters
        self.observation_space = gym.spaces.Box(
            low=-50, high=50,
            shape=(20,),  # Climate features
            dtype=np.float32
        )

        self.current_step = 0
        self.max_steps = 100

    def step(self, action):
        # Execute action (building design parameters)
        building_params = {
            'orientation': action[0],
            'wwr': action[1],
            'height': action[2],
            'length': action[3],
            'width': action[4]
        }

        # Simulate building performance
        energy_consumption = self.simulate_energy(building_params)
        comfort_score = self.calculate_comfort(building_params)
        cost = self.calculate_cost(building_params)

        # Calculate reward (minimize energy, maximize comfort, minimize cost)
        reward = -(energy_consumption * 0.5 + cost * 0.3) + comfort_score * 0.2

        self.current_step += 1
        done = self.current_step >= self.max_steps

        return self.get_observation(), reward, done, {}

    def reset(self):
        self.current_step = 0
        return self.get_observation()

    def get_observation(self):
        # Return climate and site data as observation
        return np.array(self.climate_data['features'])


class RLBuildingOptimizer:
    def __init__(self, climate_data, site_constraints):
        self.env = BuildingDesignEnv(climate_data, site_constraints)
        self.model = PPO('MlpPolicy', self.env, verbose=1)

    def train_agent(self, total_timesteps=10000):
        """Train the RL agent"""
        self.model.learn(total_timesteps=total_timesteps)

    def optimize_design(self, climate_data):
        """Use trained agent to optimize building design"""
        obs = self.env.reset()
        action, _ = self.model.predict(obs)

        return {
            'orientation': action[0],
            'window_wall_ratio': action[1],
            'height': action[2],
            'length': action[3],
            'width': action[4]
        }