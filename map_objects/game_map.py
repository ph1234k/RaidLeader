import tcod as libtcod
from random import randint

from entity import Entity
from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from components.stairs import Stairs
from dice import roll, random_choice_from_dict
from generators.monsters import MonsterGen
from map_objects.tile import Tile
from map_objects.rectangle import Rect
from render_functions import RenderOrder
from game_messages import Message

class GameMap:
	def __init__(self, width, height, dungeon_level=1):
		self.width = width
		self.height = height
		self.tiles = self.initialize_tiles()
		self.dungeon_level = dungeon_level
		self.monster_chances, self.monster_table = MonsterGen().gen_monster_table(self.dungeon_level)

	def initialize_tiles(self):
		tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

		return tiles

	def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room):
		rooms = []
		num_rooms = 0

		center_of_last_room_x = None
		center_of_last_room_y = None

		for r in range(max_rooms):
			w = randint(room_min_size, room_max_size)
			h = randint(room_min_size, room_max_size)
			x = randint(0, map_width - w - 1)
			y = randint(0, map_height - h - 1)

			new_room = Rect(x, y, w, h)
			for other_room in rooms:
				if new_room.intersect(other_room):
					break
			else:
				self.create_room(new_room)
				(new_x, new_y) = new_room.center()
				center_of_last_room_x = new_x
				center_of_last_room_y = new_y
				if num_rooms == 0:
					player.x = new_x
					player.y = new_y
				else:
					(prev_x, prev_y) = rooms[num_rooms - 1].center()
					if randint(0, 1) == 1:
						self.create_h_tunnel(prev_x, new_x, prev_y)
						self.create_v_tunnel(prev_y, new_y, prev_x)
					else:
						self.create_v_tunnel(prev_y, new_y, prev_x)
						self.create_h_tunnel(prev_x, new_x, prev_y)
				self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)
				rooms.append(new_room)
				num_rooms += 1
		# WARNING! This does NOT check if the player can reach these stairs
		down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs', render_order=RenderOrder.STAIRS,
			stairs=Stairs(self.dungeon_level + 1))
		entities.append(down_stairs)
	def create_room(self, room):
		# Go through the tiles in room and make them passable
		for x in range(room.x1 + 1, room.x2):
			for y in range(room.y1 + 1, room.y2):
				self.tiles[x][y].blocked = False
				self.tiles[x][y].block_sight = False

	def create_h_tunnel(self, x1, x2, y):
		for x in range(min(x1, x2), max(x1, x2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False

	def create_v_tunnel(self, y1, y2, x):
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False

	def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
		number_of_monsters = randint(0, max_monsters_per_room)
		number_of_items = randint(0, max_items_per_room)

		for i in range(number_of_monsters):
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				mon_template = self.monster_table[random_choice_from_dict(self.monster_chances)]
				monster = Entity(x, y, mon_template.char, mon_template.color, mon_template.name, blocks=True, render_order=RenderOrder.ACTOR, ai=BasicMonster(),
						fighter=Fighter(hp=mon_template.hp, num_die=mon_template.num_die, type_die=mon_template.type_die, mod_die=mon_template.mod_die, defense=mon_template.defense, xp=mon_template.xp))
				entities.append(monster)
		for i in range(number_of_items):
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)
			# TODO: Allow items to spawn on each other. (add: and not entity.item)
			# TDOD: Will be annoying to test though. Might bump up max items when doing so
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				d100 = randint(0, 100)
				if d100 < 70:
					item = Entity(x, y, '!', libtcod.violet, "Healing Potion", render_order=RenderOrder.ITEM,
						item=Item(use_function=heal, amount=5))
				elif d100 < 80:
					item = Entity(x, y, "?", libtcod.red, "Fireball Scroll", render_order=RenderOrder.ITEM,
						item=Item(use_function=cast_fireball, targeting=True, damage=12, radius=3,
							targeting_message=Message('Left click target tile to cast, or right click to cancel', libtcod.light_cyan)))
				elif d100 < 90:
					item = Entity(x, y, '?', libtcod.yellow, "Lightning Scroll", render_order=RenderOrder.ITEM,
						item=Item(use_function=cast_lightning, damage=20, maximum_range=5))
				else:
					item = Entity(x, y, '?', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
								  item=Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
						'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)))
				entities.append(item)

	def is_blocked(self, x, y):
		if self.tiles[x][y].blocked:
			return True

		return False

	def next_floor(self, player, message_log, constants):
		self.dungeon_level += 1
		self.monster_chances, self.monster_table = MonsterGen().gen_monster_table(self.dungeon_level)
		entities = [player]

		self.tiles = self.initialize_tiles()
		self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_room'], constants['max_items_per_room'])

		message_log.add_message(Message('Welcome to floor {0}'.format(self.dungeon_level), libtcod.light_cyan))

		return entities