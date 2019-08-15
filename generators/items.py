import tcod as libtcod

from entity import Entity
from components.equipment import EquipmentSlots
from components.equippable import Equippable
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
			'healing potion': ItemPart(char='!', color=libtcod.violet, name="Healing Potion",
						item=Item(use_function=heal, amount=50)),
			'fireball scroll': ItemPart(char='?', color=libtcod.red, name="Fireball Scroll",
						item=Item(use_function=cast_fireball, targeting=True, damage=25, radius=3,
							targeting_message=Message('Left click target tile to cast, or right click to cancel', libtcod.light_cyan))),
			'lightning scroll': ItemPart(char='?', color=libtcod.yellow, name="Lightning Scroll",
						item=Item(use_function=cast_lightning, damage=40, maximum_range=5)),
			'confusion scroll': ItemPart(char='?', color=libtcod.light_pink, name='Confusion Scroll',
								  item=Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
						'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)))
		}
		self.item_chances = {'healing potion': 75, 'fireball scroll': 10, 'lightning scroll': 5, 'confusion scroll': 5}
		
		self.tier1 = {
			'broken': ItemPart(name='broken', color=libtcod.dark_red, equippable=Equippable(None, mod_die_bonus=-2)),
			'pristine': ItemPart(name='pristine', color=libtcod.yellow, equippable=Equippable(None, mod_die_bonus=1)),
			'blessed': ItemPart(name='blessed', color=libtcod.pink, equippable=Equippable(None, mod_die_bonus=3)),
			'basic': ItemPart(name='', color=libtcod.white, equippable=Equippable(None))
		}
		self.tier1_chances = {'broken': 4, 'pristine': 4, 'blessed': 1, 'basic': 8}
		self.tier2 = {
			'sword': ItemPart(name='sword', char='/', equippable=Equippable(slot=EquipmentSlots.WEAPON, num_die_bonus=1, type_die_bonus=6))
		}
		self.tier2_chances = {'sword': 5}

	def gen_item_table(self, dungeon_level):
		self.item_chances['fireball scroll'] += 10
		self.item_chances['lightning scroll'] += 10
		self.item_chances['confusion scroll'] += 10
		if dungeon_level == 5:
			self.item_chances['healing potion'] = 50
		elif dungeon_level == 10:
			self.item_chances['healing potion'] = 25
		max_uniq_equs =  roll(1, dungeon_level)+1
		while max_uniq_equs > 0:
			self.gen_item(dungeon_level)
			max_uniq_equs -= 1
		return self.item_chances, self.items

	def gen_item(self, dungeon_level):
		t1 = self.tier1[random_choice_from_dict(self.tier1_chances)]
		t2 = self.tier2[random_choice_from_dict(self.tier2_chances)]
		uniqify = str(roll(300, 300))
		new_equipment = ItemPart()
		new_equipment.char = t2.char
		new_equipment.name = t1.name + ' ' + t2.name
		new_equipment.color = t1.color
		new_equipment.item = Item()
		new_equipment.equippable = Equippable(slot=t2.equippable.slot,
		 	max_hp_bonus=t2.equippable.max_hp_bonus+t1.equippable.max_hp_bonus,
		 	defense_bonus=t2.equippable.defense_bonus+t1.equippable.defense_bonus,
		 	num_die_bonus=t2.equippable.num_die_bonus+t1.equippable.num_die_bonus,
		 	type_die_bonus=t2.equippable.type_die_bonus+t1.equippable.type_die_bonus,
		 	mod_die_bonus=t2.equippable.mod_die_bonus+t1.equippable.mod_die_bonus)
		self.items[new_equipment.name+uniqify] = new_equipment
		self.item_chances[new_equipment.name+uniqify] = 25 * dungeon_level

class ItemPart:
	def __init__(self, char=None, color=None, name='', item=None, equippable=None):
		self.char = char
		self.color = color
		self.name = name
		self.item = item
		self.equippable = equippable
