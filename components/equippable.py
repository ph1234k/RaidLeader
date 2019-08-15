class Equippable:
	def __init__(self, slot , max_hp_bonus=0, defense_bonus=0, num_die_bonus=0, type_die_bonus=0, mod_die_bonus=0):
		self.slot = slot
		self.max_hp_bonus = max_hp_bonus
		self.defense_bonus = defense_bonus
		self.num_die_bonus = num_die_bonus
		self.type_die_bonus = type_die_bonus
		self.mod_die_bonus = mod_die_bonus