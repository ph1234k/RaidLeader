import tcod as libtcod
from components.fighter import Fighter
from components.level import Level
from components.inventory import Inventory
from entity import Entity
from game_messages import MessageLog
from game_states import GameState
from map_objects.game_map import GameMap
from render_functions import RenderOrder

def get_constants():
	window_title = "RaidLeader"
	screen_width = 80
	screen_height = 60
	
	bar_width = 20
	panel_height = 7
	panel_y = 0
	message_x = bar_width + 2
	message_width = screen_width - bar_width - 2
	message_height = panel_height - 1

	map_width = 80
	map_height = 52

	room_max_size = 10
	room_min_size = 6
	max_rooms = 30

	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 10

	max_monsters_per_room = 3
	max_items_per_room = 2

	colors = {
		'dark_wall': libtcod.Color(80, 80, 80),
		'dark_ground': libtcod.Color(140, 120, 100),
		'light_wall': libtcod.Color(130, 130, 130),
		'light_ground': libtcod.Color(200, 180, 140)
	}

	constants = {
		'window_title': window_title,
		'screen_width': screen_width,
		'screen_height': screen_height,
		'bar_width': bar_width,
		'panel_height': panel_height,
		'panel_y': panel_y,
		'message_width': message_width,
		'message_height': message_height,
		'message_x': message_x,
		'map_width': map_width,
		'map_height': map_height,
		'room_min_size': room_min_size,
		'room_max_size': room_max_size,
		'max_rooms': max_rooms,
		'fov_algorithm': fov_algorithm,
		'fov_light_walls': fov_light_walls,
		'fov_radius': fov_radius,
		'max_monsters_per_room': max_monsters_per_room,
		'max_items_per_room': max_items_per_room,
		'colors': colors
	}

	return constants

def get_game_variables(constants):
	player = Entity(0, 0, '@', libtcod.pink, "Player", blocks=True, render_order=RenderOrder.ACTOR, 
		fighter=Fighter(hp=100, num_die=2, type_die=6, mod_die=2, defense=4), inventory=Inventory(52), level=Level())
	entities = [player]
	game_map = GameMap(constants['map_width'], constants['map_height'])
	game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_room'], constants['max_items_per_room'])
	message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])
	game_state = GameState.PLAYER_TURN
	
	return player, entities, game_map, message_log, game_state