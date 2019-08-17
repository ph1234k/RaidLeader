import tcod as libtcod

from entity import Entity
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.item import Item
from components.item_functions import heal, cast_confuse, cast_fireball, cast_lightning
from game_messages import Message
from dice import roll, random_choice_from_dict, from_dungeon_level

class ItemGen:
	# Initial idea here is to gen an item, and afterwards we correct x and y. 
	# If this doesn't work I'll create an ItemPart class that holds Item()
	#   as well as color and character data
	# My only concern to test is whether or not these end up being linked. 
	def __init__(self, dungeon_level):
		self.dungeon_level = dungeon_level
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
		
		self.weapon_attribute = {
			'broken': ItemPart(name='broken', color=libtcod.dark_red, equippable=Equippable(None, mod_die_bonus=-2)),
			'pristine': ItemPart(name='pristine', color=libtcod.yellow, equippable=Equippable(None, mod_die_bonus=1)),
			'blessed': ItemPart(name='blessed', color=libtcod.pink, equippable=Equippable(None, mod_die_bonus=3)),
			'basic': ItemPart(name='', color=libtcod.white, equippable=Equippable(None))
		}
		self.weapon_attribute_chances = {'broken': 4, 'pristine': 4, 'blessed': 1, 'basic': 8}
		self.weapon_material = {
			'bronze': ItemPart(name='bronze', equippable=Equippable(None, mod_die_bonus=5)),
			'silver': ItemPart(name='silver', equippable=Equippable(None, mod_die_bonus=10))
		}
		self.weapon_material_chances = {'bronze': 5, 'silver': 5}
		self.weapon_type = {
			'sword': ItemPart(name='sword', char='/', equippable=Equippable(slot=EquipmentSlots.WEAPON, num_die_bonus=1, type_die_bonus=6)),
			'dagger': ItemPart(name='dagger', char='-', equippable=Equippable(slot=EquipmentSlots.WEAPON, num_die_bonus=1, type_die_bonus=4)),
			'mace': ItemPart(name='mace', char='|', equippable=Equippable(slot=EquipmentSlots.WEAPON, num_die_bonus=1, type_die_bonus=12)),
			'axe': ItemPart(name='axe', char='\\', equippable=Equippable(slot=EquipmentSlots.WEAPON, num_die_bonus=1, type_die_bonus=8))
		}
		self.weapon_type_chances = {'axe': 5, 'sword': 5, 'dagger': 5, 'mace': from_dungeon_level([[5, 7]], self.dungeon_level)}
		self.armor_attribute = {
			'light': ItemPart(name='light', equippable=Equippable(None, num_die_bonus=1, defense_bonus=-10)),
			'heavy': ItemPart(name='heavy', equippable=Equippable(None, num_die_bonus=-2, defense_bonus=50)),
			'blessed': ItemPart(name='blessed', equippable=Equippable(None, max_hp_bonus=50))
		}
		self.armor_attribute_chances = {'light': 5, 'heavy': 5, 'blessed': 5}
		self.armor_material = {
			'leather': ItemPart(name='leather', color=libtcod.Color(165, 42, 42), equippable=Equippable(None, max_hp_bonus=10, defense_bonus=1)),
			'copper': ItemPart(name='copper', color=libtcod.Color(204, 118, 0), equippable=Equippable(None, max_hp_bonus=25, defense_bonus=2)),
			'silver': ItemPart(name='silver', color=libtcod.Color(192, 192, 192), equippable=Equippable(None, max_hp_bonus=50, defense_bonus=5))
		}
		self.armor_material_chances = {'leather': 5, 'copper': 5, 'silver': 5}
		self.armor_type = {
			'helmet': ItemPart(name='helmet', char='+', equippable=Equippable(slot=EquipmentSlots.HEAD)),
			'tunic': ItemPart(name='tunic', char='8', equippable=Equippable(slot=EquipmentSlots.CHEST)),
			'gloves': ItemPart(name='gloves', char='*', equippable=Equippable(slot=EquipmentSlots.GLOVES)),
			'pants': ItemPart(name='pants', char='4', equippable=Equippable(slot=EquipmentSlots.LEGS)),
			'boots': ItemPart(name='boots', char=':', equippable=Equippable(slot=EquipmentSlots.BOOTS))
		}
		self.armor_type_chances = {'helmet': 5, 'tunic': 5, 'gloves': 5, 'pants': 5, 'boots': 5} 
		self.jewelery_attribute = {
			'speed': ItemPart(name='of speed', equippable=Equippable(None, num_die_bonus=1)),
			'health': ItemPart(name='of health', equippable=Equippable(None, max_hp_bonus=40)),
			'defense': ItemPart(name='of defense', equippable=Equippable(None, defense_bonus=10)),
			'bigweapon': ItemPart(name='of giant weapon', equippable=Equippable(None, type_die_bonus=4)),
			'damage': ItemPart(name='of damage', equippable=Equippable(None, mod_die_bonus=10))
		} 
		self.jewelery_attribute_chances = {'speed': 5, 'health': 5, 'defense': 5, 'bigweapon': 5, 'damage': 5}
		self.jewelery_material = {
			'copper': ItemPart(name='copper', color=libtcod.Color(204, 118, 0), equippable=Equippable(None, defense_bonus=1)),
			'silver': ItemPart(name='silver', color=libtcod.Color(192, 192, 192), equippable=Equippable(None, defense_bonus=10))
		}
		self.jewelery_material_chances = {'copper': 5, 'silver': 5}
		self.jewelery_type = {
			'ring': ItemPart(name='ring', char='o', equippable=Equippable(EquipmentSlots.LEFT_RING)),
			'necklace': ItemPart(name='necklace', char='v', equippable=Equippable(slot=EquipmentSlots.NECK))
		}
		self.jewelery_type_chances = {'ring': 5, 'necklace': 5}

	def gen_item_table(self):
		self.item_chances['fireball scroll'] += 10
		self.item_chances['lightning scroll'] += 10
		self.item_chances['confusion scroll'] += 10
		if self.dungeon_level == 5:
			self.item_chances['healing potion'] = 50
		elif self.dungeon_level == 10:
			self.item_chances['healing potion'] = 25
		max_uniq_equs =  roll(2, self.dungeon_level+3)+5
		while max_uniq_equs > 0:
			self.gen_item(self.dungeon_level)
			max_uniq_equs -= 1
		return self.item_chances, self.items

	def gen_item(self, dungeon_level):
		item_types = {'weapon': 5, 'armor': 5, 'jewelery': 5}
		item_type = random_choice_from_dict(item_types)
		if item_type == 'weapon':
			t1 = self.weapon_attribute[random_choice_from_dict(self.weapon_attribute_chances)]
			t2 = self.weapon_type[random_choice_from_dict(self.weapon_type_chances)]
			t3 = self.weapon_material[random_choice_from_dict(self.weapon_material_chances)]
			uniqify = str(roll(300, 300))
			new_equipment = ItemPart()
			extra_mod_die_damage = roll(1 + int(dungeon_level / 3), 3+dungeon_level)
			new_equipment.char = t2.char
			new_equipment.name = '+' + str(extra_mod_die_damage) + ' ' + t1.name + ' ' + t3.name + ' ' + t2.name
			new_equipment.color = t1.color
			new_equipment.item = Item()
			new_equipment.equippable = Equippable(slot=t2.equippable.slot,
			 	max_hp_bonus=t2.equippable.max_hp_bonus+t1.equippable.max_hp_bonus+t2.equippable.max_hp_bonus,
			 	defense_bonus=t2.equippable.defense_bonus+t1.equippable.defense_bonus+t3.equippable.defense_bonus,
			 	num_die_bonus=t2.equippable.num_die_bonus+t1.equippable.num_die_bonus+t3.equippable.num_die_bonus,
			 	type_die_bonus=t2.equippable.type_die_bonus+t1.equippable.type_die_bonus+t3.equippable.type_die_bonus,
			 	mod_die_bonus=t2.equippable.mod_die_bonus+t1.equippable.mod_die_bonus+t3.equippable.mod_die_bonus+extra_mod_die_damage)
			self.items[new_equipment.name+uniqify] = new_equipment
			self.item_chances[new_equipment.name+uniqify] = 25 * dungeon_level
		elif item_type == 'armor':
			attrib = self.armor_attribute[random_choice_from_dict(self.armor_attribute_chances)]
			arm_type = self.armor_type[random_choice_from_dict(self.armor_type_chances)]
			mat = self.armor_material[random_choice_from_dict(self.armor_material_chances)]
			extra_defense = roll(1+int(dungeon_level/3), 3+dungeon_level)
			uniqify = str(roll(300, 300))
			new_equipment = ItemPart()
			new_equipment.name = '+' + str(extra_defense) + ' ' + attrib.name + ' ' + mat.name + ' ' + arm_type.name
			new_equipment.char = arm_type.char
			new_equipment.color = mat.color
			new_equipment.item = Item()
			new_equipment.equippable = Equippable(slot=arm_type.equippable.slot,
				max_hp_bonus=attrib.equippable.max_hp_bonus + mat.equippable.max_hp_bonus + arm_type.equippable.max_hp_bonus,
				defense_bonus=attrib.equippable.defense_bonus + mat.equippable.defense_bonus + arm_type.equippable.defense_bonus + extra_defense,
				num_die_bonus=attrib.equippable.num_die_bonus + mat.equippable.num_die_bonus + arm_type.equippable.num_die_bonus,
				type_die_bonus=attrib.equippable.type_die_bonus + mat.equippable.type_die_bonus + arm_type.equippable.type_die_bonus,
				mod_die_bonus=attrib.equippable.mod_die_bonus + mat.equippable.mod_die_bonus + arm_type.equippable.mod_die_bonus)
			self.items[new_equipment.name+uniqify] = new_equipment
			self.item_chances[new_equipment.name+uniqify] = 25 * dungeon_level
		elif item_type == 'jewelery':
			attrib = self.jewelery_attribute[random_choice_from_dict(self.jewelery_attribute_chances)]
			jew_type = self.jewelery_type[random_choice_from_dict(self.jewelery_type_chances)]
			mat = self.jewelery_material[random_choice_from_dict(self.jewelery_material_chances)]
			uniqify = str(roll(300, 300))
			extra_hp = roll(1+int(dungeon_level/3), 3+dungeon_level) * 10
			new_equipment = ItemPart()
			new_equipment.name = '+' + str(extra_hp) + ' ' +mat.name + ' ' + jew_type.name + ' ' + attrib.name
			new_equipment.char = jew_type.char
			new_equipment.color = mat.color
			new_equipment.item = Item()
			new_equipment.equippable = Equippable(slot=jew_type.equippable.slot,
				max_hp_bonus=attrib.equippable.max_hp_bonus+mat.equippable.max_hp_bonus+jew_type.equippable.max_hp_bonus+extra_hp,
				defense_bonus=attrib.equippable.defense_bonus+mat.equippable.defense_bonus+jew_type.equippable.defense_bonus,
				num_die_bonus=attrib.equippable.num_die_bonus+mat.equippable.num_die_bonus+jew_type.equippable.num_die_bonus,
				type_die_bonus=attrib.equippable.type_die_bonus+mat.equippable.num_die_bonus+jew_type.equippable.num_die_bonus,
				mod_die_bonus=attrib.equippable.mod_die_bonus+mat.equippable.mod_die_bonus+jew_type.equippable.mod_die_bonus)
			self.items[new_equipment.name+uniqify] = new_equipment
			self.item_chances[new_equipment.name+uniqify] = 25 + dungeon_level

class ItemPart:
	def __init__(self, char=None, color=None, name='', item=None, equippable=None):
		self.char = char
		self.color = color
		self.name = name
		self.item = item
		self.equippable = equippable
