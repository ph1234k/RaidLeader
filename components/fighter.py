import tcod as libtcod
from dice import roll
from game_messages import Message

class Fighter:

	def __init__(self, hp, num_die, type_die, mod_die, defense, xp=0):
		self.max_hp = hp
		self.hp = hp
		# The die variables will work as follows
		# Damage = XDY+Z
		# Where X is num_die, Y is type_die and Z is mod_die
		self.num_die = num_die
		self.type_die = type_die
		self.mod_die = mod_die
		self.defense = defense
		self.xp = xp

	def take_damage(self, amount):
		results = []

		self.hp -= amount
		if self.hp > self.max_hp:
			self.hp = self.max_hp
		elif self.hp <= 0:
			self.hp = 0
			results.append({'dead': self.owner, 'xp': self.xp})
		
		return results

	def attack(self, target):
		results = []
		damage = (roll(self.num_die, self.type_die) + self.mod_die) - target.fighter.defense
		if damage > 0:
			results.append({'message': Message('{0} hits {1} for {2} damage!'.format(self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
			results.extend(target.fighter.take_damage(damage))
		else:
			results.append({'message': Message('{0} hit {1}, but did no damage.'.format(self.owner.name.capitalize(), target.name), libtcod.white)})

		return results