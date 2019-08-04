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

def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
	# Shows a menu with each item of inventory as an option
	if len(inventory.items) == 0:
		options = ['Inventory is empty.']
	else:
		options = [item.name for item in inventory.items]
	menu(con, header, options, inventory_width, screen_width, screen_height)