import tcod as libtcod

def menu(con, header, options, width, screen_width, screen_height):
	# Check for number of options, need 52 or less. 
	if len(options) > 52: raise ValueError('Cannot have more than 52 options')

	# Calculate header height
	header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
	height = len(options) + header_height

	#create off screen console for the menu
	window = libtcod.console_new(width, height)

	# Print header, with auto-wrap
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

	# Print all options
	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ') ' + option_text
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		if letter_index == ord('z'):
			letter_index = ord('A')
		else:
			letter_index += 1

	# Blit contents
	x = int(screen_width / 2 - width / 2)
	y = int(screen_height / 2 - height / 2)
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
	# Shows a menu with each item of inventory as an option
	if len(player.inventory.items) == 0:
		options = ['Inventory is empty.']
	else:
		options = []
		for item in player.inventory.items:
			if player.equipment.weapon == item:
				options.append('{0} (wielded)'.format(item.name))
			elif player.equipment.head == item or player.equipment.chest == item or player.equipment.neck == item or player.equipment.gloves == item or player.equipment.legs == item or player.equipment.boots == item or player.equipment.left_ring == item or player.equipment.right_ring == item:
				options.append('{0} (worn)'.format(item.name))
			else:
				options.append(item.name)
	menu(con, header, options, inventory_width, screen_width, screen_height)

def main_menu(con, background_image, screen_width, screen_height):
	libtcod.image_blit_2x(background_image, 0, 0, 0)

	libtcod.console_set_default_foreground(0, libtcod.light_yellow)
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
		"RaidLeader - Nenomanto")
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
		"By Stephanie Rice")

	menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)

def message_box(con, header, width, screen_width, screen_height):
	menu(con, header, [], width, screen_width, screen_height)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
	options = ['Health. New HP: {0}'.format(player.fighter.max_hp+20),
		'Defense. New Defense: {0}'.format(player.fighter.defense+1),
		'Power. New Damage: {0}d{1} + {2}'.format(player.fighter.num_die,player.fighter.type_die,player.fighter.mod_die+1),
		'Speed. New Speed: {0}'.format(player.fighter.speed)]

	menu(con, header, options, menu_width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}d{1}+{2}'.format(player.fighter.num_die, player.fighter.type_die, player.fighter.mod_die))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)
