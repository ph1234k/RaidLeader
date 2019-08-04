import tcod as libtcod
from random import randint

from entity import Entity
from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.item_functions import heal, cast_lightning
from map_objects.tile import Tile
from map_objects.rectangle import Rect
from render_functions import RenderOrder

class GameMap:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.tiles = self.initialize_tiles()

	def initialize_tiles(self):
		tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

		return tiles

	def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room):
		rooms = []
		num_rooms = 0

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
				d100 = randint(0, 100)
				if d100 < 80:
					monster = Entity(x, y, 'Z', libtcod.darker_green, "Zombie", blocks=True, render_order=RenderOrder.ACTOR, ai=BasicMonster(),
						fighter=Fighter(hp=12, power=3, defense=1))
				else:
					monster = Entity(x, y, 'z', libtcod.black, "Rotting Zombie", blocks=True, render_order=RenderOrder.ACTOR, ai=BasicMonster(),
						fighter=Fighter(hp=8, power=6, defense=0))
				entities.append(monster)
		for i in range(number_of_items):
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)
			# TODO: Allow items to spawn on each other. (add: and not entity.item)
			# TDOD: Will be annoying to test though. Might bump up max items when doing so
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				d100 = randint(0, 100)
				if d100 < 75:
					item = Entity(x, y, '6', libtcod.violet, "Healing Potion", render_order=RenderOrder.ITEM,
						item=Item(use_function=heal, amount=5))
				else:
					item = Entity(x, y, '!', libtcod.yellow, "Lightning Scroll", render_order=RenderOrder.ITEM,
						item=Item(use_function=cast_lightning, damage=20, maximum_range=5))
				entities.append(item)

	def is_blocked(self, x, y):
		if self.tiles[x][y].blocked:
			return True

		return False

