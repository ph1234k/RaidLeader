import tcod as libtcod
from dice import roll, random_choice_from_dict

class MonsterGen:

	def __init__(self):
		self.tier1 = {
			'angry': MonsterPart(color=libtcod.red, name='angry', defense=-1, mod_die=3, xp=10)
		}
		self.tier1_chances = {'angry': 1}
		self.tier2 = {
			'zombie': MonsterPart(char='Z', name='zombie', hp=10, num_die=1, type_die=4, defense=1, xp=35)
		}
		self.tier2_chances = {'zombie': 1}
		self.tier3 = {
			'warrior': MonsterPart(name='warrior', defense=1, hp=2, mod_die=1)
		}
		self.tier3_chances = {'warrior': 1}

	def gen_monster_table(self, dungeon_level):
		# Returns two dictionaries
		# One is a lookup of weights for use in random_choice_from_dict
		# The other contains the data needed to place each monster
		#
		# monster = Entity(x, y, 'z', libtcod.black, "Rotting Zombie", blocks=True, render_order=RenderOrder.ACTOR, ai=BasicMonster(),
		#					fighter=Fighter(hp=8, num_die=1, type_die=6, mod_die=1, defense=0, xp=100))
		#
		# One monster entry needs:
		# Character for drawing monster
		# Color of character
		# Name of monster
		# HP
		# Defense
		# num_die, type_die, mod_die
		# XP
		monster_chances = {}
		monster_table = {}
		num_uniq_mons = roll(1, (roll(2, 3)+1)) + 2
		while len(monster_table) < num_uniq_mons:
			CR = roll(1, 3) * dungeon_level
			new_mon = self.gen_monster(CR)
			uniqify = str(roll(300, 300) + CR)
			monster_table[new_mon.name + uniqify] = new_mon
			monster_chances[new_mon.name + uniqify] = 10

		return monster_chances, monster_table

	def gen_monster(self, CR):
		# Roll base stats
		monster = MonsterPart()
		monster.hp = roll(5, 5) + CR
		monster.defense = roll(1, CR)
		monster.num_die = int(CR/3)
		monster.mod_die = roll(1, CR)
		monster.xp = CR * 25
		choice1 = self.tier1[random_choice_from_dict(self.tier1_chances)]
		choice2 = self.tier2[random_choice_from_dict(self.tier2_chances)]
		choice3 = self.tier3[random_choice_from_dict(self.tier3_chances)]
		monster.color = choice1.color
		monster.name = choice1.name + ' ' + choice2.name + ' ' + choice3.name
		monster.char = choice2.char
		monster.hp = monster.hp + choice1.hp + choice2.hp + choice3.hp
		monster.defense = monster.defense + choice1.defense + choice2.defense + choice3.defense
		monster.num_die = monster. num_die + choice1.num_die + choice2.num_die + choice3.num_die
		monster.type_die = monster.type_die + choice1.type_die + choice2.type_die + choice3.type_die
		monster.mod_die = monster.mod_die + choice1.mod_die + choice2.mod_die + choice3.mod_die
		monster.xp = monster.xp + choice1.xp + choice2.xp + choice3.xp
		return monster

class MonsterPart:

	def __init__(self, char=None, color=None, name='', hp=0, defense=0, num_die=0, type_die=0, mod_die=0, xp=0):
		self.char = char
		self.color = color
		self.name = name
		self.hp = hp
		self.defense = defense
		self.num_die = num_die
		self.type_die = type_die
		self.mod_die = mod_die
		self.xp = xp