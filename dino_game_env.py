import gym
from gym import spaces


class DinoGameEnv(gym.Env):
  def __init__(self):
    # 1 = jump, 2 = duck, 3 = do nothing
    self.action_space = spaces.Discrete(3)

  def step(self, action):
    pass

  def reset(self):
    pass

  def render(self, mode='human'):
    pass

  def close(self):
    pass