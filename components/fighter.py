import tcod as libtcod
from dice import roll
from game_messages import Message

class Fighter:

	def __init__(self, hp, num_die, type_die, mod_die, defense, speed=0, xp=0):
		self.base_max_hp = hp
		self.hp = hp
		# The die variables will work as follows
		# Damage = XDY+Z
		# Where X is num_die, Y is type_die and Z is mod_die
		self.base_num_die = num_die
		self.base_type_die = type_die
		self.base_mod_die = mod_die
		self.base_defense = defense
		self.speed = speed
		self.xp = xp
		self.invis = False

	@property
	def max_hp(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.max_hp_bonus
		else:
			bonus = 0	
		return self.base_max_hp + bonus

	@property
	def defense(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.defense_bonus
		else:
			bonus = 0	
		return self.base_defense + bonus

	@property
	def num_die(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.num_die_bonus + int((self.speed+self.owner.equipment.speed_bonus) / 3)
		else:
			bonus = 0	
		return self.base_num_die + bonus

	@property
	def type_die(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.type_die_bonus
		else:
			bonus = 0	
		return self.base_type_die + bonus

	@property
	def mod_die(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.mod_die_bonus
		else:
			bonus = 0	
		return self.base_mod_die + bonus

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

	def toggle_invis(self):
		if self.invis == True:
			self.invis = False
		else:
			self.invis = True