import tcod as libtcod
from random import randint

from entity import Entity
from components.ai import BasicMonster, SwarmMonster
from components.fighter import Fighter
from components.item import Item
from components.item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from components.stairs import Stairs
from dice import roll, random_choice_from_dict, from_dungeon_level
from generators.monsters import MonsterGen
from generators.items import ItemGen
from map_objects.tile import Tile
from map_objects.rectangle import Rect
from map_objects.prefab import PFRoom, PFBigRoom, PFDiningHall
from render_functions import RenderOrder
from game_messages import Message
from math import sqrt

class GameMap:
	def __init__(self, width, height, entities, dungeon_level=1):
		self.width = width
		self.height = height
		self.tiles = self.initialize_tiles()
		self.dungeon_level = dungeon_level
		self.monster_chances, self.monster_table = MonsterGen(self.dungeon_level).gen_monster_table(entities)
		self.item_chances, self.item_table = ItemGen(self.dungeon_level).gen_item_table()
		self.north, self.south, self.east, self.west = (0, -1), (0, 1), (1, 0), (-1, 0)
		self.winding_percent = 35
		self.connection_chance = 20

	def initialize_tiles(self):
		tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

		return tiles

	def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
		rooms = []
		num_rooms = 0
		self.current_region = 0

		if map_width % 2 == 0: map_width -= 1
		if map_height % 2 == 0: map_height -= 1

		center_of_last_room_x = None
		center_of_last_room_y = None

		for r in range(max_rooms * self.dungeon_level):
			w = randint(room_min_size, room_max_size)
			h = randint(room_min_size, room_max_size)
			x = (randint(0, map_width - w - 1)//2)*2+1
			y = (randint(0, map_height - h - 1)//2)*2+1
			if x % 2 != 0:
				x += 1
			if y % 2 != 0:
				y += 1

			if roll(1, 100) > 10:
				new_room = Rect(x, y, w, h)
				prefab = False
			else:
				pf_picker = roll(1, 100)
				if pf_picker < 20: 
					new_room = PFRoom(x, y)
				elif pf_picker < 40:
					new_room = PFDiningHall(x, y)
				elif pf_picker < 101:
					new_room = PFBigRoom(x, y)
				if new_room.x2 > map_width or new_room.y2 > map_height:
					new_room = Rect(x, y, w, h)
					prefab = False
				else:
					prefab=True

			for other_room in rooms:
				if new_room.intersect(other_room):
					break
			else:
				self.create_room(new_room, prefab)
				(new_x, new_y) = new_room.center()
				center_of_last_room_x = new_x
				center_of_last_room_y = new_y
				if num_rooms == 0:
					player.x = new_x
					player.y = new_y
				self.place_entities(new_room, entities)
				rooms.append(new_room)
				num_rooms += 1
				self.current_region += 1
		down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs', render_order=RenderOrder.STAIRS,
			stairs=Stairs(self.dungeon_level + 1))
		entities.append(down_stairs)
		#for y in range(1, map_height, 14):
		for y in range(3, map_height, 2):
			for x in range(3, map_width, 2):
				if self.tiles[x][y].blocked == False:
					continue
				start = (x, y)
				self.add_maze(start, map_width, map_height)
				break
		self.connect_regions(map_width, map_height)
		self.remove_dead_ends(map_width, map_height)
		if not self.is_path_to(player, down_stairs, entities):
			entities.remove(down_stairs)
			return False
		else:
			return True

	def create_room(self, room, prefab=False):
		# check for prefab
		if prefab:
			for x in range(room.x1, room.x2-1):
				for y in range(room.y1, room.y2-1):
					#print(room.x1, room.y1)
					#print(room.x2, room.y2)
					#print(x, y)
					if room.cells[x-room.x1][y-room.y1] == 1:
						if x < self.width and y < self.height:
							self.carve(x, y)	
			return		

		# Go through the tiles in room and make them passable
		for x in range(room.x1 + 1, room.x2):
			for y in range(room.y1 + 1, room.y2):
				self.carve(x, y)

	def add_maze(self, start, map_width, map_height):
		cells = []
		last_direction = None
		self.current_region += 1
		if self.can_carve(start, (0,0), map_width, map_height):
			self.carve(start[0], start[1])
			cells.append(start)

		while cells:
			cell = cells[-1]

			unmade_cells = set()

			for direction in [self.north, self.south, self.east, self.west]:
				if self.can_carve(cell, direction, map_width, map_height):
					unmade_cells.add(direction)
			if (unmade_cells):
				if (last_direction in unmade_cells) and roll(1, 100) > self.winding_percent:
					direction = last_direction
				else:
					while direction not in unmade_cells:
						direction = random_choice_from_dict({(1, 0): 1, (-1, 0): 1, (0, 1): 1, (0, -1): 1})

				new_cell = ((cell[0]+direction[0]),(cell[1]+direction[1]))
				self.carve(new_cell[0], new_cell[1])
				cells.append(new_cell)

				last_direction = direction
			else:
				cells.pop()
				last_direction = None

	def connect_regions(self, map_width, map_height):
		connector_regions = [[None for y in range(map_height)] for x in range(map_width)]
		for x in range(1, map_width-1):
			for y in range(1, map_height-1):
				if self.tiles[x][y].blocked == False: continue

				regions = set()
				for direction in [self.north, self.south, self.east, self.west]:
					new_x = x + direction[0]
					new_y = y + direction[1]
					if self.tiles[new_x][new_y].blocked == False:
						region = self.tiles[new_x][new_y].region
						regions.add(region)
				if len(regions) < 2: continue

				connector_regions[x][y] = regions

		connectors = set()
		for x in range(0, map_width):
			for y in range(0, map_height):
				if connector_regions[x][y]:
					connectors.add((x, y))
		merged = {}
		open_regions = set()
		for i in range(0, self.current_region):
			merged[i] = i
			open_regions.add(i)

		# connect the regions
		while len(connectors) > 1:
			# get random connector
			connector = connectors.pop()
			#for connector in connectors: break

			# carve the connection
			self.addJunction(connector)

			# merge the connected regions
			x = connector[0]
			y = connector[1]
			
			# make a list of the regions at (x,y)
			regions = []
			for n in connector_regions[x][y]:
				# get the regions in the form of merged[n]
				actual_region = merged[n]
				regions.append(actual_region)
				
			dest = regions[0]
			sources = regions[1:]

			'''
			Merge all of the effective regions. You must look
			at all of the regions, as some regions may have
			previously been merged with the ones we are
			connecting now.
			'''
			for i in range(self.current_region):
				#if merged[i] in sources:
					merged[i] = dest

			# clear the sources, they are no longer needed
			for s in sources:
			#	if s in open_regions:
					open_regions.remove(s)
			# remove the unneeded connectors
			to_be_removed = set()
			for pos in connectors:
				# remove connectors that are next to the current connector
				if self.distance(connector,pos) < 2:
					# remove it
					to_be_removed.add(pos)
					continue

				regions = set()
				x = pos[0]
				y = pos[1]
				for n in connector_regions[x][y]:
					if n in merged:
						actual_region = merged[n]
						regions.add(actual_region)
				if len(regions) > 1: 
					continue

				if roll(1, 100) < self.connection_chance:
					self.addJunction(pos)

				# remove it
				if len(regions) == 1:
					to_be_removed.add(pos)

			connectors.difference_update(to_be_removed)

	def remove_dead_ends(self, map_width, map_height):
		done = False
		emergency = 500
		while not done:
			#print('loop iter: ', 99 - emergency)
			to_remove = [[0 for y in range(map_height)] for x in range(map_width)]
			done = True
			for y in range(map_height):
				for x in range(map_width):
					if self.tiles[x][y].blocked == False:
						for direction in [self.north, self.south, self.east, self.west]:
							if self.tiles[x+direction[0]][y+direction[1]].blocked == True: 
								to_remove[x][y] += 1
					if to_remove[x][y] > 2:
						self.tiles[x][y].blocked = True
						self.tiles[x][y].block_sight = True
						self.tiles[x][y].region = 0
						done = False
					if x-1 > 0 and y-1 > 0:
						da_sum = to_remove[x][y]+to_remove[x-1][y]+to_remove[x][y-1]+to_remove[x-1][y-1]
						#if emergency == 100 :print(to_remove[x][y],to_remove[x-1][y],to_remove[x][y-1],to_remove[x-1][y-1], da_sum)
						if da_sum > 5:
							if self.tiles[x][y].blocked == False and self.tiles[x-1][y].blocked == False and self.tiles[x][y-1].blocked == False and self.tiles[x-1][y-1].blocked == False:
								self.tiles[x][y].blocked = True
								self.tiles[x][y].block_sight = True
								self.tiles[x][y].region = 0
								self.tiles[x-1][y].blocked = True
								self.tiles[x-1][y].block_sight = True
								self.tiles[x-1][y].region = 0
								self.tiles[x][y-1].blocked = True
								self.tiles[x][y-1].block_sight = True
								self.tiles[x][y-1].region = 0
								self.tiles[x-1][y-1].blocked = True
								self.tiles[x-1][y-1].block_sight = True
								self.tiles[x-1][y-1].region = 0
								done = False
								#print('REACHED')
			if emergency <= 0:
				print("WARN: EMERGENCY ESCAPE REACHED IN REMOVE DEAD ENDS")
				done = True
			emergency -= 1



	def carve(self, x, y):
		self.tiles[x][y].blocked = False
		self.tiles[x][y].block_sight = False
		self.tiles[x][y].region = self.current_region

	def addJunction(self, pos):
		self.carve(pos[0], pos[1])

	def can_carve(self, pos, dire, map_width, map_height):
		x = pos[0]+dire[0] # If east and pos is (1, 1) then 
		y = pos[1]+dire[1] # x, y = 4, 1

		if not (0 < x < map_width) or not (0 < y < map_height):
			return False

		x = pos[0]+dire[0] # x, y = 2, 1
		y = pos[1]+dire[1]

		for direction in [self.north, self.east, self.west, self.south]:
			dest_x = x + direction[0]
			dest_y = y + direction[1]
			if (pos[0], pos[1]) != (dest_x, dest_y):
			#if self.tiles[pos[0]][pos[1]].region != self.tiles[dest_x][dest_y].region: # City-like
				if self.tiles[dest_x][dest_y].blocked == False:
					return False

		return self.tiles[x][y].blocked

	def distance(self, a, b):
		pre_dist = (a[0]-b[0])**2 + (a[1]-b[1])**2
		if (pre_dist * -1) > pre_dist:
			pre_dist = pre_dist * -1
		distance = sqrt(pre_dist)

		return distance

	def place_entities(self, room, entities):
		max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
		max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)
		number_of_monsters = randint(0, max_monsters_per_room)
		number_of_items = randint(0, max_items_per_room)

		for i in range(number_of_monsters):
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				mon_template = self.monster_table[random_choice_from_dict(self.monster_chances)]
				if mon_template.ai_type == 'swarm':
					new_ai = SwarmMonster(entities)
				else:
					new_ai = BasicMonster()
				monster = Entity(x, y, mon_template.char, mon_template.color, mon_template.name, blocks=True, render_order=RenderOrder.ACTOR, ai=new_ai,
						fighter=Fighter(hp=mon_template.hp, num_die=mon_template.num_die, type_die=mon_template.type_die, mod_die=mon_template.mod_die, defense=mon_template.defense, xp=mon_template.xp))
				entities.append(monster)
		for i in range(number_of_items):
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)
			# TODO: Allow items to spawn on each other. (add: and not entity.item)
			# TDOD: Will be annoying to test though. Might bump up max items when doing so
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				item_template = self.item_table[random_choice_from_dict(self.item_chances)]
				item = Entity(x, y, item_template.char, item_template.color, item_template.name, render_order=RenderOrder.ITEM,
				 item=item_template.item, equippable=item_template.equippable)
				entities.append(item)

	def is_blocked(self, x, y):
		if x >= self.width or y >= self.height or x < 0 or y < 0:
			return True
		if self.tiles[x][y].blocked:
			return True

		return False

	def next_floor(self, player, message_log, constants):
		entities = [player]
		self.dungeon_level += 1
		self.monster_chances, self.monster_table = MonsterGen(self.dungeon_level).gen_monster_table(entities)
		self.item_chances, self.item_table = ItemGen(self.dungeon_level).gen_item_table()

		self.tiles = self.initialize_tiles()
		succeed = self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities)
		if not succeed:
			return False
		message_log.add_message(Message('Welcome to floor {0}'.format(self.dungeon_level), libtcod.light_cyan))

		return entities

	def is_path_to(self, source, target, entities):
		result = False
		# Create a FOV map that has the dimensions of the map
		fov = libtcod.map_new(self.width, self.height)

		# Scan the current map each turn and set all the walls as unwalkable
		for y1 in range(self.height):
			for x1 in range(self.width):
				libtcod.map_set_properties(fov, x1, y1, not self.tiles[x1][y1].block_sight,
										   not self.tiles[x1][y1].blocked)

		# Scan all the objects to see if there are objects that must be navigated around
		# Check also that the object isn't self or the target (so that the start and the end points are free)
		# The AI class handles the situation if self is next to the target so it will not use this A* function anyway
		for entity in entities:
			if entity.blocks and entity != self and entity != target:
				# Set the tile as a wall so it must be navigated around
				libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

		# Allocate a A* path
		# The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
		my_path = libtcod.path_new_using_map(fov, 1.41)

		# Compute the path between self's coordinates and the target's coordinates
		libtcod.path_compute(my_path, source.x, source.y, target.x, target.y)

		# Check if the path exists
		if not libtcod.path_is_empty(my_path):
			result = True

		# Delete the path to free memory
		libtcod.path_delete(my_path)
		return result
