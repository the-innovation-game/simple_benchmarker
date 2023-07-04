from scipy.interpolate import interp1d
import random
import numpy as np
import hashlib
import logging

logging.basicConfig(format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("the-innovation-game")
logger.setLevel(logging.INFO)

GIT_REPO = "https://github.com/the-innovation-game/challenges.git"
GIT_BRANCH = "alpha"


class IntermediateIntegersLogger:
    def __init__(self):
        self.logs = []
    
    def log(self, v: int):
        self.logs.append(int(v))
        
    def dump(self):
        max_log_len = 10
        log_len = min(len(self.logs), max_log_len)
        if log_len == 0:
            return []
        step_increment = len(self.logs) / log_len
        return [
            (step, self.logs[step - 1]) 
            for step in [
                int((i + 1) * step_increment)
                for i in range(log_len)
            ]
        ]

def calcSeed(player_id: str, block_id: str, prev_block_id: str, algorithm_id: str, challenge_id: str, difficulty: dict, nonce: int) -> int:
    seed_phrase = f"{player_id},{block_id},{prev_block_id},{algorithm_id},{challenge_id},{sorted(difficulty.items())},{nonce}"
    return int.from_bytes(hashlib.sha256(seed_phrase.encode()).digest()[-4:], "big")

def randomInterpolate(points, min_point):
    min_x, min_y = min_point
    max_x = max(x for x, y in points)
    max_y = max(y for x, y in points)
    
    points = set(tuple(p) for p in points)
    # Add points right on the bounds so we can interpolate across the full x and y range
    if not any(x == min_x for x, y in points):
        points.add((min_x, max_y))
    if not any(y == min_y for x, y in points):
        points.add((max_x, min_y))
    
    # Interpolate a random x, y point
    if len(points) < 2:
        random_x, random_y = list(points)[0]
    elif 0.5 < random.random():
        # random x, interpolate y
        f = interp1d(
            [x for x, y in points],
            [y for x, y in points]
        )
        random_x = random.randint(min_x, max_x)
        random_y = int(np.round(f(random_x)))
    else:
        # random y, interpolate x
        f = interp1d(
            [y for x, y in points],
            [x for x, y in points]
        )
        random_y = random.randint(min_y, max_y)
        random_x = int(np.round(f(random_y)))

    return random_x, random_y