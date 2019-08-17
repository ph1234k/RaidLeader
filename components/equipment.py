from enum import Enum, auto

class EquipmentSlots(Enum):
	WEAPON = auto()
	HEAD = auto()
	CHEST = auto()
	GLOVES = auto()
	BOOTS = auto()
	LEGS = auto()
	LEFT_RING = auto()
	RIGHT_RING = auto()
	NECK = auto()


class Equipment:
	def __init__(self, weapon=None, head=None, neck=None, chest=None, gloves=None, legs=None, boots=None, left_ring=None, right_ring=None):
		self.weapon = weapon
		self.head = head
		self.neck = neck
		self.chest = chest
		self.gloves = gloves
		self.legs = legs
		self.boots = boots
		self.left_ring = left_ring
		self.right_ring = right_ring

	@property
	def max_hp_bonus(self):
		bonus = 0
		if self.weapon and self.weapon.equippable:
			bonus += self.weapon.equippable.max_hp_bonus
		if self.head and self.head.equippable:
			bonus += self.head.equippable.max_hp_bonus
		if self.neck and self.neck.equippable:
			bonus += self.neck.equippable.max_hp_bonus
		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.max_hp_bonus
		if self.gloves and self.gloves.equippable:
			bonus += self.gloves.equippable.max_hp_bonus
		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.max_hp_bonus
		if self.boots and self.boots.equippable:
			bonus += self.boots.equippable.max_hp_bonus
		if self.left_ring and self.left_ring.equippable:
			bonus += self.left_ring.equippable.max_hp_bonus
		if self.right_ring and self.right_ring.equippable:
			bonus += self.right_ring.equippable.max_hp_bonus

		return bonus

	@property
	def defense_bonus(self):
		bonus = 0
		if self.weapon and self.weapon.equippable:
			bonus += self.weapon.equippable.defense_bonus
		if self.head and self.head.equippable:
			bonus += self.head.equippable.defense_bonus
		if self.neck and self.neck.equippable:
			bonus += self.neck.equippable.defense_bonus
		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.defense_bonus
		if self.gloves and self.gloves.equippable:
			bonus += self.gloves.equippable.defense_bonus
		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.defense_bonus
		if self.boots and self.boots.equippable:
			bonus += self.boots.equippable.defense_bonus
		if self.left_ring and self.left_ring.equippable:
			bonus += self.left_ring.equippable.defense_bonus
		if self.right_ring and self.right_ring.equippable:
			bonus += self.right_ring.equippable.defense_bonus

		return bonus

	@property
	def num_die_bonus(self):
		bonus = 0
		if self.weapon and self.weapon.equippable:
			bonus += self.weapon.equippable.num_die_bonus
		if self.head and self.head.equippable:
			bonus += self.head.equippable.num_die_bonus
		if self.neck and self.neck.equippable:
			bonus += self.neck.equippable.num_die_bonus
		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.num_die_bonus
		if self.gloves and self.gloves.equippable:
			bonus += self.gloves.equippable.num_die_bonus
		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.num_die_bonus
		if self.boots and self.boots.equippable:
			bonus += self.boots.equippable.num_die_bonus
		if self.left_ring and self.left_ring.equippable:
			bonus += self.left_ring.equippable.num_die_bonus
		if self.right_ring and self.right_ring.equippable:
			bonus += self.right_ring.equippable.num_die_bonus

		return bonus

	@property
	def type_die_bonus(self):
		bonus = 0
		if self.weapon and self.weapon.equippable:
			bonus += self.weapon.equippable.type_die_bonus
		if self.head and self.head.equippable:
			bonus += self.head.equippable.type_die_bonus
		if self.neck and self.neck.equippable:
			bonus += self.neck.equippable.type_die_bonus
		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.type_die_bonus
		if self.gloves and self.gloves.equippable:
			bonus += self.gloves.equippable.type_die_bonus
		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.type_die_bonus
		if self.boots and self.boots.equippable:
			bonus += self.boots.equippable.type_die_bonus
		if self.left_ring and self.left_ring.equippable:
			bonus += self.left_ring.equippable.type_die_bonus
		if self.right_ring and self.right_ring.equippable:
			bonus += self.right_ring.equippable.type_die_bonus

		return bonus

	@property
	def mod_die_bonus(self):
		bonus = 0
		if self.weapon and self.weapon.equippable:
			bonus += self.weapon.equippable.mod_die_bonus
		if self.head and self.head.equippable:
			bonus += self.head.equippable.mod_die_bonus
		if self.neck and self.neck.equippable:
			bonus += self.neck.equippable.mod_die_bonus
		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.mod_die_bonus
		if self.gloves and self.gloves.equippable:
			bonus += self.gloves.equippable.mod_die_bonus
		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.mod_die_bonus
		if self.boots and self.boots.equippable:
			bonus += self.boots.equippable.mod_die_bonus
		if self.left_ring and self.left_ring.equippable:
			bonus += self.left_ring.equippable.mod_die_bonus
		if self.right_ring and self.right_ring.equippable:
			bonus += self.right_ring.equippable.mod_die_bonus
		return bonus

	@property
	def speed_bonus(self):
		bonus = 0
		if self.weapon and self.weapon.equippable:
			bonus += self.weapon.equippable.speed_bonus
		if self.head and self.head.equippable:
			bonus += self.head.equippable.speed_bonus
		if self.neck and self.neck.equippable:
			bonus += self.neck.equippable.speed_bonus
		if self.chest and self.chest.equippable:
			bonus += self.chest.equippable.speed_bonus
		if self.gloves and self.gloves.equippable:
			bonus += self.gloves.equippable.speed_bonus
		if self.legs and self.legs.equippable:
			bonus += self.legs.equippable.speed_bonus
		if self.boots and self.boots.equippable:
			bonus += self.boots.equippable.speed_bonus
		if self.left_ring and self.left_ring.equippable:
			bonus += self.left_ring.equippable.speed_bonus
		if self.right_ring and self.right_ring.equippable:
			bonus += self.right_ring.equippable.speed_bonus

		return bonus

	def toggle_equip(self, equippable_entity):
		results = []

		slot = equippable_entity.equippable.slot

		if slot == EquipmentSlots.WEAPON:
			if self.weapon == equippable_entity:
				self.weapon = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.weapon:
					results.append({'dequipped': self.weapon})

				self.weapon = equippable_entity
				results.append({'equipped': equippable_entity})
		elif slot == EquipmentSlots.HEAD:
			if self.head == equippable_entity:
				self.head = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.head:
					results.append({'dequipped': self.head})

				self.head = equippable_entity
				results.append({'equipped': equippable_entity})
		elif slot == EquipmentSlots.CHEST:
			if self.chest == equippable_entity:
				self.chest = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.chest:
					results.append({'dequipped': self.chest})

				self.chest = equippable_entity
				results.append({'equipped': equippable_entity})
		elif slot == EquipmentSlots.NECK:
			if self.neck == equippable_entity:
				self.neck = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.neck:
					results.append({'dequipped': self.neck})

				self.neck = equippable_entity
				results.append({'equipped': equippable_entity})
		elif slot == EquipmentSlots.GLOVES:
			if self.gloves == equippable_entity:
				self.gloves = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.gloves:
					results.append({'dequipped': self.gloves})

				self.gloves = equippable_entity
				results.append({'equipped': equippable_entity})
		elif slot == EquipmentSlots.BOOTS:
			if self.boots == equippable_entity:
				self.boots = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.boots:
					results.append({'dequipped': self.boots})

				self.boots = equippable_entity
				results.append({'equipped': equippable_entity})
		elif slot == EquipmentSlots.LEGS:
			if self.legs == equippable_entity:
				self.legs = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.legs:
					results.append({'dequipped': self.legs})

				self.legs = equippable_entity
				results.append({'equipped': equippable_entity})
		elif slot == EquipmentSlots.LEFT_RING or slot == EquipmentSlots.RIGHT_RING:
			if self.left_ring == None:
				if self.right_ring == equippable_entity:
					self.right_ring = None
					results.append({'dequipped': equippable_entity})
				else:
					self.left_ring = equippable_entity
					results.append({'equipped': equippable_entity})
			else: 
				if self.right_ring == None:
					if self.left_ring == equippable_entity:
						self.left_ring = None
						results.append({'dequipped': self.left_ring})
					else:
						self.right_ring = equippable_entity
						results.append({'equipped': equippable_entity})
				elif self.left_ring and self.right_ring:
					if self.right_ring == equippable_entity:
						self.right_ring = None
						results.append({'dequipped': equippable_entity})
					elif self.left_ring == equippable_entity:
						self.left_ring = None
						results.append({'dequipped': equippable_entity})
					else:
						results.append({'dequipped': self.left_ring})
						self.left_ring = equippable_entity
						results.append({'equipped': equippable_entity})
		return results