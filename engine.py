import tcod as libtcod
from game_states import GameState
from entity import get_blocking_entities_at_location
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from render_functions import clear_all, render_all, RenderOrder
from game_messages import Message
from fov_functions import initialize_fov, recompute_fov
from death_functions import kill_player, kill_monster
from dice import roll

def main():
	constants = get_constants()
	
	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

	libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False, renderer=libtcod.RENDERER_SDL2, vsync=False)

	con = libtcod.console.Console(constants['screen_width'], constants['screen_height'])
	panel = libtcod.console.Console(constants['screen_width'], constants['panel_height'])

	player, entities, game_map, message_log, game_state = None, [], None, None, None
	
	show_main_menu = True
	show_load_error_message = False

	main_menu_background_image = libtcod.image_load('menu_background.png')

	key = libtcod.Key()
	mouse = libtcod.Mouse()

	while True:
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

		if show_main_menu:
			main_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'])

			if show_load_error_message:
				message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'])

			libtcod.console_flush()

			action = handle_main_menu(key)

			new_game = action.get('new_game')
			load_saved_game = action.get('load_game')
			exit_game = action.get('exit')

			if show_load_error_message and (new_game or load_saved_game or exit_game):
				show_load_error_message = False
			elif new_game:
				player, entities, game_map, message_log, game_state = get_game_variables(constants)
				game_state = GameState.PLAYER_TURN
				show_main_menu = False
			elif load_saved_game:
				try:
					player, entities, game_map, message_log, game_state = load_game()
					show_main_menu = False
				except FileNotFoundError:
					show_load_error_message = True
			elif exit_game:
				break

		else:
			libtcod.console_clear(con)
			play_game(player, entities, game_map, message_log, game_state, con, panel, constants)

			show_main_menu = True


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants):
	fov_recompute = True
	fov_map = initialize_fov(game_map)
	key = libtcod.Key()
	mouse = libtcod.Mouse()
	previous_game_state = game_state
	targeting_item = None

	while not libtcod.console_is_window_closed():
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])
		render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)
		fov_recompute = False
		libtcod.console_flush()

		clear_all(con, entities)

		action = handle_keys(key, game_state)
		mouse_action = handle_mouse(mouse)

		move = action.get('move')
		pickup = action.get('pickup')
		exit = action.get('exit')
		fullscreen = action.get('fullscreen')
		show_inventory = action.get('show_inventory')
		drop_inventory = action.get('drop_inventory')
		inventory_index = action.get('inventory_index')
		wait = action.get('wait')
		take_stairs = action.get('take_stairs')
		eat = action.get('eat')
		level_up = action.get('level_up')
		show_character_screen = action.get('show_character_screen')

		left_click = mouse_action.get('left_click')
		right_click = mouse_action.get('right_click')

		player_turn_results = []

		if move and game_state == GameState.PLAYER_TURN:
			dx, dy = move
			dest_x = player.x + dx
			dest_y = player.y + dy

			if not game_map.is_blocked(dest_x, dest_y):
				target = get_blocking_entities_at_location(entities, dest_x, dest_y)
				if target:
					player_turn_results.extend(player.fighter.attack(target))
				else:
					player.move(dx, dy)
					fov_recompute = True
				game_state = GameState.ENEMY_TURN

		if pickup and game_state==GameState.PLAYER_TURN:
			for entity in entities:
				if entity.item and entity.x == player.x and entity.y == player.y:
					pickup_results = player.inventory.add_item(entity)
					player_turn_results.extend(pickup_results)
					break
			else:
				message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

		if show_inventory:
			previous_game_state = game_state
			game_state = GameState.SHOW_INVENTORY

		if drop_inventory:
			previous_game_state = game_state
			game_state = GameState.DROP_INVENTORY

		if inventory_index is not None and previous_game_state != GameState.PLAYER_DEAD and inventory_index < len(player.inventory.items):
			item = player.inventory.items[inventory_index]
			if game_state == GameState.SHOW_INVENTORY:
				player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
			elif game_state == GameState.DROP_INVENTORY:
				player_turn_results.extend(player.inventory.drop_item(item))

		if wait:
			player.fighter.take_damage(-5)
			game_state = GameState.ENEMY_TURN

		if eat:
			for entity in entities:
				if entity.render_order == RenderOrder.CORPSE and (entity.x == player.x and entity.y == player.y):
					player_turn_results.append({'consume_corpse': entity})
					break
			else:
				message_log.add_message(Message('There is nothing to eat here.', libtcod.yellow))

		if take_stairs and game_state == GameState.PLAYER_TURN:
			for entity in entities:
				if entity.stairs and entity.x == player.x and entity.y == player.y:
					entities = game_map.next_floor(player, message_log, constants)
					fov_map = initialize_fov(game_map)
					fov_recompute = True
					libtcod.console_clear(con)

					break
			else:
				message_log.add_message(Message('There are no stairs here.', libtcod.yellow))
		if level_up:
			if level_up == 'hp':
				player.fighter.base_max_hp += 20
				player.fighter.hp += 20
			elif level_up == 'def':
				player.fighter.base_defense += 1
			elif level_up == 'str':
				if roll(1, 3) == 3:
					player.fighter.base_num_die += 1 + roll(1, 3)
					player.fighter.base_type_die += 1 + roll(1, 3)
				player.fighter.base_mod_die += 1
			game_state = GameState.ENEMY_TURN

		if game_state == GameState.TARGETING:
			if left_click:
				target_x, target_y = left_click
				target_y -= 8
				item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
					target_x=target_x, target_y=target_y)
				player_turn_results.extend(item_use_results)
			elif right_click:
				player_turn_results.append({'targeting_cancelled': True})

		if show_character_screen:
			previous_game_state = game_state
			game_state = GameState.CHARACTER_SCREEN

		if exit:
			if game_state in (GameState.SHOW_INVENTORY, GameState.DROP_INVENTORY, GameState.CHARACTER_SCREEN):
				game_state = previous_game_state
			elif game_state == GameState.TARGETING:
				player_turn_results.append({'targeting_cancelled': True})
			else:
				save_game(player, entities, game_map, message_log, game_state)
				return True

		if fullscreen:
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

		for player_turn_result in player_turn_results:
			message = player_turn_result.get('message')
			dead_entity = player_turn_result.get('dead')
			item_added = player_turn_result.get('item_added')
			item_consumed = player_turn_result.get('consumed')
			item_dropped = player_turn_result.get('item_dropped')
			targeting = player_turn_result.get('targeting')
			targeting_cancelled = player_turn_result.get('targeting_cancelled')
			consume_corpse = player_turn_result.get('consume_corpse')
			xp = player_turn_result.get('xp')
			equip = player_turn_result.get('equip')

			if message:
				message_log.add_message(message)
			if dead_entity:
				if dead_entity == player:
					message, game_state = kill_player(dead_entity)
				else:
					message = kill_monster(dead_entity)
				message_log.add_message(message)
			if item_added:
				entities.remove(item_added)
				game_state = GameState.ENEMY_TURN
			if item_consumed:
				game_state = GameState.ENEMY_TURN
			if item_dropped:
				entities.append(item_dropped)
				game_state = GameState.ENEMY_TURN
			if targeting:
				previous_game_state = GameState.PLAYER_TURN
				game_state = GameState.TARGETING

				targeting_item = targeting
				message_log.add_message(targeting_item.item.targeting_message)
			if targeting_cancelled:
				game_state = previous_game_state
				message_log.add_message(Message('Targeting has been cancelled.'))
			if consume_corpse:
				player.fighter.take_damage(-50)
				message_log.add_message(Message('You eat the {0} and gain some strength.'.format(consume_corpse.name)))
				player.fighter.base_defense += consume_corpse.defense
				entities.remove(consume_corpse)
				game_state = GameState.ENEMY_TURN
			if xp:
				leveled_up = player.level.add_xp(xp)
				message_log.add_message(Message('You gain {0} XP!'.format(xp), libtcod.cyan))
				if leveled_up:
					message_log.add_message(Message('Your skills grow stronger. You reached level {0}!'.format(player.level.current_level), libtcod.green))
					previous_game_state = game_state
					game_state = GameState.LEVEL_UP
			if equip:
				equip_results = player.equipment.toggle_equip(equip)

				for equip_result in equip_results:
					equipped = equip_result.get('equipped')
					dequipped = equip_result.get('dequipped')
					if equipped:
						message_log.add_message(Message('You equipped the {0}'.format(equipped.name)))
					if dequipped:
						message_log.add_message(Message('You dequipped the {0}'.format(dequipped.name)))
				game_state = GameState.ENEMY_TURN

		if game_state == GameState.ENEMY_TURN:
			for entity in entities:
				if entity.ai:
					enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
					for enemy_turn_result in enemy_turn_results:
						message = enemy_turn_result.get('message')
						dead_entity = enemy_turn_result.get('dead')

						if message:
							message_log.add_message(message)
						if dead_entity:
							if dead_entity == player:
								message, game_state = kill_player(dead_entity)
							else:
								message = kill_monster(dead_entity)
							message_log.add_message(message)
							if game_state == GameState.PLAYER_DEAD:
								break
				if game_state == GameState.PLAYER_DEAD:
					break

			else:
				game_state = GameState.PLAYER_TURN

	
if __name__ == '__main__':
	main()