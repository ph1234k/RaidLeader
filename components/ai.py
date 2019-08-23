import tcod as libtcod
from random import randint
from game_messages import Message
from entity import Entity
from dice import roll

class BasicMonster:
	def take_turn(self, target, fov_map, game_map, entities):
		results = []

		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if target.fighter.invis == False:
				if monster.distance_to(target) >= 2:
					monster.move_astar(target, entities, game_map)
				elif target.fighter.hp > 0:
					results.extend(monster.fighter.attack(target))
			else:
				#target = entities[roll(1, len(entities)-1)]
				monster.move_towards((roll(1, 3)-2+monster.x), (roll(1, 3)-2+monster.y) , game_map, entities)
		else:
			#target = entities[roll(1, len(entities)-1)]
			monster.move_towards((roll(1, 3)-2+monster.x), (roll(1, 3)-2+monster.y) , game_map, entities)

		return results

	def get_name(self):
		pass


class ConfusedMonster:
	"""docstring for ConfusedMonster"""
	def __init__(self, previous_ai, num_turns=10):
		self.previous_ai = previous_ai
		self.num_turns = num_turns
		
	def take_turn(self, target, fov_map, game_map, entities):
		results = []

		if self.num_turns > 0:
			random_x = self.owner.x + randint(0, 2) - 1
			random_y = self.owner.y + randint(0, 2) - 1
			if random_x != self.owner.x or random_y != self.owner.y:
				self.owner.move_towards(random_x, random_y, game_map, entities)
			self.num_turns -= 1
		else:
			self.owner.ai = self.previous_ai
			results.append({'message': Message('The {0} is no longer cofused.'.format(self.owner.name), libtcod.red)})

		return results

	def get_name(self):
		pass

class SwarmMonster:
	def __init__(self, entities):
		self.queen = None
		for entity in entities:
			if entity.ai:
				if entity.ai.get_name() == 'queen':
					self.name = 'worker'
					self.queen = entity
					break
		else:
			self.name = 'queen'

	def take_turn(self, target, fov_map, game_map, entities):
		monster = self.owner
		if not libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			for entity in entities:
				if entity.ai:
					if entity.ai.get_name() == 'queen':
						if entity != self.owner:
							self.name = 'worker'
							self.queen = entity
							break
			else:
				self.name = 'queen'
				self.queen = None
		if self.name == 'queen':
			return self.take_turn_queen(target, fov_map, game_map, entities)
		elif self.name == 'worker':
			return self.take_turn_worker(target, fov_map, game_map, entities)			

	def get_name(self):
		return self.name

	def take_turn_worker(self, target, fov_map, game_map, entities):
		results = []

		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if target.fighter.invis == False:
				if monster.distance_to(target) >= 2:
					monster.move_astar(target, entities, game_map)
				elif target.fighter.hp > 0:
					results.extend(monster.fighter.attack(target))
			else:
				#target = entities[roll(1, len(entities)-1)]
				if monster.distance_to(target) >= 2:
					monster.move_astar(self.queen, entities, game_map)
				else:
					pass
		else:
			#target = entities[roll(1, len(entities)-1)]
			if monster.distance_to(target) >= 2:
				monster.move_astar(self.queen, entities, game_map)
			else:
				pass
		return results

	def take_turn_queen(self, target, fov_map, game_map, entities):
		results = []

		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if target.fighter.invis == False:
				if monster.distance_to(target) >= 2:
					monster.move_astar(target, entities, game_map)
				elif target.fighter.hp > 0:
					results.extend(monster.fighter.attack(target))
			else:
				#target = entities[roll(1, len(entities)-1)]
				monster.move_towards((roll(1, 3)-2+monster.x), (roll(1, 3)-2+monster.y) , game_map, entities)
		else:
			#target = entities[roll(1, len(entities)-1)]
			monster.move_towards((roll(1, 3)-2+monster.x), (roll(1, 3)-2+monster.y) , game_map, entities)

		return results