import tcod as libtcod

from game_states import GameState
from render_functions import RenderOrder
from game_messages import Message

def kill_player(player):
	player.char = '%'
	player.color = libtcod.dark_red

	return Message('You died!', libtcod.red), GameState.PLAYER_DEAD

def kill_monster(monster):
	death_message = Message('{0} died!'.format(monster.name.capitalize()), libtcod.orange)

	monster.char = '%'
	monster.color = libtcod.dark_red
	monster.blocks = False
	monster.defense = monster.fighter.defense
	monster.fighter = None
	monster.ai = None
	monster.name = 'remains of ' + monster.name
	monster.render_order = RenderOrder.CORPSE

	return death_message