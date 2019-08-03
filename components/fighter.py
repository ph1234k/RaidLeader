class Fighter:

	def __init__(self, hp, power, defense):
		self.max_hp = hp
		self.hp = hp
		self.power = power
		self.defense = defense

	def take_damage(self, amount):
		results = []

		self.hp -= amount
		if self.hp > self.max_hp:
			self.hp = self.max_hp
		elif self.hp < 0:
			self.hp = 0
			results.append({'dead': self.owner})
		
		return results

	def attack(self, target):
		results = []
		damage = self.power - target.fighter.defense
		if damage > 0:
			results.append({'message': '{0} hits {1} for {2} damage!'.format(self.owner.name.capitalize(), target.name, str(damage))})
			results.extend(target.fighter.take_damage(damage))
		else:
			results.append({'message': '{0} hit {1}, but did no damage.'.format(self.owner.name.capitalize(), target.name)})

		return results