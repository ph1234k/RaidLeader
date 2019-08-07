import tcod as libtcod
from game_states import GameState
from entity import Entity, get_blocking_entities_at_location
from components.fighter import Fighter
from components.inventory import Inventory
from input_handlers import handle_keys, handle_mouse
from render_functions import clear_all, render_all, RenderOrder
from game_messages import MessageLog, Message
from fov_functions import initialize_fov, recompute_fov
from death_functions import kill_player, kill_monster
from map_objects.game_map import GameMap

def main():
	screen_width = 80
	screen_height = 50
	
	bar_width = 20
	panel_height = 7
	panel_y = screen_height - panel_height
	message_x = bar_width + 2
	message_width = screen_width - bar_width - 2
	message_height = panel_height - 1

	map_width = 80
	map_height = 43

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
		'dark_ground': libtcod.Color(120, 120, 120),
		'light_wall': libtcod.Color(130, 130, 130),
		'light_ground': libtcod.Color(180, 180, 180)
	}

	player = Entity(0, 0, '@', libtcod.pink, "Player", blocks=True, render_order=RenderOrder.ACTOR, 
		fighter=Fighter(hp=30, power=5, defense=2), inventory=Inventory(52))
	entities = [player]

	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

	libtcod.console_init_root(screen_width, screen_height, 'NewRL', False)

	con = libtcod.console_new(screen_width, screen_height)
	panel = libtcod.console_new(screen_width, panel_height)
	game_map = GameMap(map_width, map_height)
	game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room)
	fov_recompute = True
	fov_map = initialize_fov(game_map)
	message_log = MessageLog(message_x, message_width, message_height)
	key = libtcod.Key()
	mouse = libtcod.Mouse()
	game_state = GameState.PLAYER_TURN
	previous_game_state = game_state
	targeting_item = None

	while not libtcod.console_is_window_closed():
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, fov_radius)
		render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state)
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
			game_state = GameState.ENEMY_TURN

		if game_state == GameState.TARGETING:
			if left_click:
				target_x, target_y = left_click
				item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
					target_x=target_x, target_y=target_y)
				player_turn_results.extend(item_use_results)
			elif right_click:
				player_turn_results.append({'targeting_cancelled': True})

		if exit:
			if game_state in (GameState.SHOW_INVENTORY, GameState.DROP_INVENTORY):
				game_state = previous_game_state
			elif game_state == GameState.TARGETING:
				player_turn_results.append({'targeting_cancelled': True})
			else:
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