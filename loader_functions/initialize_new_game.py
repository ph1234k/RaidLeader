import tcod as libtcod
from components.equipment import Equipment, EquipmentSlots
from components.equippable import Equippable
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
	max_rooms = 10
	#max_rooms = 200

	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 10

	colors = {
		'dark_wall': libtcod.Color(20, 20, 20),
		'dark_ground': libtcod.Color(140, 120, 100),
		'light_wall': libtcod.Color(90, 90, 90),
		'light_ground': libtcod.Color(210, 190, 150)
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
		'colors': colors
	}

	return constants

def get_game_variables(constants):
	player = Entity(0, 0, '@', libtcod.pink, "Player", blocks=True, render_order=RenderOrder.ACTOR, 
		fighter=Fighter(hp=100, num_die=2, type_die=4, mod_die=6, defense=20), inventory=Inventory(52), level=Level(), equipment=Equipment())
	entities = [player]
	starting_dagger = Entity(0, 0, '-', libtcod.sky, 'Dagger', equippable=Equippable(EquipmentSlots.WEAPON, num_die_bonus=1, type_die_bonus=4), render_order=RenderOrder.ITEM)
	player.inventory.add_item(starting_dagger)
	player.equipment.toggle_equip(starting_dagger)
	game_map = GameMap(constants['map_width'], constants['map_height'], entities)
	map_make_success = game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities)
	while not map_make_success:
		game_map = GameMap(constants['map_width'], constants['map_height'], entities)
		map_make_success = game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities)
	message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])
	game_state = GameState.PLAYER_TURN
	
	return player, entities, game_map, message_log, game_state