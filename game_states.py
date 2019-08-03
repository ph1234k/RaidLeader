from enum import Enum

class GameState(Enum):
	PLAYER_TURN = 1
	ENEMY_TURN = 2
	PLAYER_DEAD = 3