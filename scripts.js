const getTrexInfo = () => {
  const { tRex } = Runner.instance_;

  return {
    xPos: tRex.xPos,
    yPos: tRex.yPos,
    isJumping: tRex.jumping,
    isDucking: tRex.ducking,
  };
};

const getNextObstacle = () => {
  const { obstacles } = Runner.instance_.horizon;

  if (!obstacles.length) return null;

  const obstacle = obstacles[0];

  return {
    gap: obstacle.gap || -1, // distance between the next object
    size: obstacle.size || -1,
    xPos: obstacle.xPos || -1,
    yPos: obstacle.yPos || -1,
    height: obstacle.typeConfig.height || -1,
    width: obstacle.typeConfig.width || -1,
  };
};

const getCurrentSpeed = () => Runner.instance_.currentSpeed.toFixed(4);

const getCurrentScore = () => {
  const score = Runner.instance_.distanceMeter.digits.join("");

  if (!score) return 0;

  return Number.parseInt(score, 10);
};

const getGameObservation = () => {
  const tRex = getTrexInfo();
  const nextObstacle = getNextObstacle();
  const currentSpeed = getCurrentSpeed();

  return [
    tRex.xPos,
    tRex.yPos,
    currentSpeed,
    nextObstacle.gap,
    nextObstacle.size,
    nextObstacle.xPos,
    nextObstacle.yPos,
    nextObstacle.height,
    nextObstacle.width,
  ];
};
