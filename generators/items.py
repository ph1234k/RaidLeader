import tcod as libtcod

from entity import Entity
from components.item import Item
from components.item_functions import heal, cast_confuse, cast_fireball, cast_lightning
from game_messages import Message
from dice import roll, random_choice_from_dict

class ItemGen:
	# Initial idea here is to gen an item, and afterwards we correct x and y. 
	# If this doesn't work I'll create an ItemPart class that holds Item()
	#   as well as color and character data
	# My only concern to test is whether or not these end up being linked. 
	def __init__(self):
		self.items = {
			'healing potion': ItemPart('!', libtcod.violet, "Healing Potion",
						item=Item(use_function=heal, amount=50)),
			'fireball scroll': ItemPart('?', libtcod.red, "Fireball Scroll",
						item=Item(use_function=cast_fireball, targeting=True, damage=12, radius=3,
							targeting_message=Message('Left click target tile to cast, or right click to cancel', libtcod.light_cyan))),
			'lightning scroll': ItemPart('?', libtcod.yellow, "Lightning Scroll",
						item=Item(use_function=cast_lightning, damage=20, maximum_range=5)),
			'confusion scroll': ItemPart('?', libtcod.light_pink, 'Confusion Scroll',
								  item=Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
						'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)))
		}
		self.item_chances = {'healing potion': 75, 'fireball scroll': 10, 'lightning scroll': 5, 'confusion scroll': 5}

	def gen_item_table(self, dungeon_level):
		self.item_chances['fireball scroll'] += 10
		self.item_chances['lightning scroll'] += 10
		self.item_chances['confusion scroll'] += 10
		if dungeon_level == 5:
			self.item_chances['healing potion'] = 50
		elif dungeon_level == 10:
			self.item_chances['healing potion'] = 25

		return self.item_chances, self.items

class ItemPart:
	def __init__(self, char, color, name, item=None):
		self.char = char
		self.color = color
		self. name = name
		self.item = item