import gym
import numpy as np
from gym import spaces
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class DinoGameEnv(gym.Env):
  def __init__(self, headless=True):
    # 0 = do nothing, 1 = jump, 2 = duck
    self.action_space = spaces.Discrete(3)
    self.observation_space = spaces.Box(low=-50, high=np.inf, shape=(9,), dtype=np.float32)
    self.headless = headless
    self._setupWebdriver()

  def step(self, action):
    if action == 1:
      self._sendKey(Keys.SPACE)
    elif action == 2:
      self._sendKey(Keys.DOWN)
    else:
      pass

    observation = self.get_observation()
    done = self._isGameOver()
    reward = 1 if not done else -10

    return observation, reward, done, {}


  def reset(self):
    self.driver.execute_script("Runner.instance_.stop()")
    self.driver.execute_script("Runner.instance_.restart()")
    self.get_observation()

  def get_observation(self):
    return self._getGameObservation()

  def render(self, mode='human'):
    pass

  def close(self):
    self.driver.close()

  def _setupWebdriver(self):
    options = Options()
    options.add_argument("--mute-audio")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if self.headless:
      options.add_argument("--headless")
      options.add_argument("--disable-gpu")

    self.driver = webdriver.Chrome(options=options)
    self.driver.set_window_size(1600, 900)

    # needs to be in try/except block otherwise it won't start the game
    try:
      self.driver.get('chrome://dino')
    except WebDriverException:
      pass

    self._sendKey(Keys.SPACE)

  def _isGameOver(self):
    return self.driver.execute_script("return Runner.instance_.crashed")

  def _getTrexInfo(self):
    return self.driver.execute_script("""const getTrexInfo = () => {
      const { tRex } = Runner.instance_;

      return {
        xPos: tRex.xPos,
        yPos: tRex.yPos,
        isJumping: tRex.jumping,
        isDucking: tRex.ducking,
      };
    };

    return getTrexInfo();"""
    )

  def _getNextObstacle(self):
    return self.driver.execute_script("""const getNextObstacle = () => {
      const { obstacles } = Runner.instance_.horizon;
      const obstacle = obstacles[0];

      return {
        gap: obstacle?.gap || -1, // distance between the next object
        size: obstacle?.size || -1,
        xPos: obstacle?.xPos || -1,
        yPos: obstacle?.yPos || -1,
        height: obstacle?.typeConfig.height || -1,
        width: obstacle?.typeConfig.width || -1,
      };
    };
    
    return getNextObstacle();"""
    )

  def _getCurrentSpeed(self):
    return self.driver.execute_script("Runner.instance_.currentSpeed.toFixed(4);")

  def _getGameObservation(self):
    trex = self._getTrexInfo()
    current_speed = self._getCurrentSpeed()
    next_obstacle = self._getNextObstacle()


    return [
      trex["xPos"],
      trex["yPos"],
      current_speed,
      next_obstacle["gap"],
      next_obstacle["size"],
      next_obstacle["xPos"],
      next_obstacle["yPos"],
      next_obstacle["height"],
      next_obstacle["width"],
    ]

  def _sendKey(self, key):
    self.driver.find_element(By.TAG_NAME, "body").send_keys(key)
