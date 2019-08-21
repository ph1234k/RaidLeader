import tcod as libtcod
from dice import roll, random_choice_from_dict, from_dungeon_level

class MonsterGen:

	def __init__(self, dungeon_level):
		self.dungeon_level = dungeon_level
		self.tier1 = {
			'angry': MonsterPart(color=libtcod.red, 
				name=''.join((chr(libtcod.COLCTRL_5) , 'angry', chr(libtcod.COLCTRL_STOP))), 
				defense=-1, mod_die=5, xp=10),
			'berserk': MonsterPart(color=libtcod.orange, 
				name=''.join((chr(libtcod.COLCTRL_4), 'berserk', chr(libtcod.COLCTRL_STOP))), 
				defense=-5, num_die=3, mod_die=5, xp=50),
			'drowsy': MonsterPart(color=libtcod.blue, name='drowsy', hp=50, defense=5, xp=10),
			'rotting': MonsterPart(color=libtcod.black, name='rotting', hp=-10, defense=-1, mod_die=10, type_die=1, xp=50),
			'quick': MonsterPart(color=libtcod.violet, name='quick', num_die=2, xp=20),
			'lucky': MonsterPart(color=libtcod.green, 
				name=''.join((chr(libtcod.COLCTRL_2),'lucky',chr(libtcod.COLCTRL_STOP))),
				xp=777),
			'deadly': MonsterPart(color=libtcod.light_cyan, name='deadly', num_die=2, type_die=6, mod_die=5, xp=5000, hp=50, defense=25)
		}
		self.tier1_chances = {'angry': 3, 'berserk': 3, 'drowsy': 3, 'rotting': 3, 'quick': 3, 'lucky': 1, 'deadly': from_dungeon_level([[1, 5]], self.dungeon_level)}
		self.tier2 = {
			'zombie': MonsterPart(char='Z', name='zombie', hp=10, num_die=1, type_die=4, defense=1, xp=35),
			'kobold': MonsterPart(char='k', name='kobold', hp=15, num_die=1, type_die=6, defense=3, xp=50),
			'rat': MonsterPart(char='r', name='rat', hp=5, num_die=1, type_die=3, xp=10),
			'orc': MonsterPart(char='O', name='orc', hp=50, num_die=1, type_die=8, defense=5, xp=150),
			'dragon': MonsterPart(char='D', name='dragon', hp=100, num_die=4, type_die=6, mod_die=5, defense=15, xp=200),
			'snorklefarker': MonsterPart(char='S', name='snorklefarker', hp=1000, num_die=8, type_die=12, mod_die=8, defense=100, xp=5000, chance_table=-5)
		}
		self.tier2_chances = {'zombie': 6, 'kobold': 6, 'rat': 6, 'orc': 4, 'dragon': from_dungeon_level([[2, 5]], self.dungeon_level), 'snorklefarker': from_dungeon_level([[1, 10]], self.dungeon_level)}
		self.tier3 = {
			'warrior': MonsterPart(name='warrior', defense=1, hp=2, mod_die=1),
			'obliterator': MonsterPart(name='obliterator', mod_die=10, xp=25),
			'worshipper': MonsterPart(name='worshipper', mod_die=4, num_die=1, defense=3, xp=10),
			'basic': MonsterPart(hp=40),
			'demigod': MonsterPart(name='demigod', hp=1000, defense=100, xp=500)
		}
		self.tier3_chances = {'warrior': 2, 'obliterator': 2, 'worshipper': 2, 'basic': 4, 'demigod': from_dungeon_level([[1, 10]], self.dungeon_level)}

	def gen_monster_table(self):
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
			CR = roll(1, 3) * self.dungeon_level
			new_mon = self.gen_monster(CR)
			uniqify = str(roll(300, 300) + CR)
			monster_table[new_mon.name + uniqify] = new_mon
			monster_chances[new_mon.name + uniqify] = 10 + new_mon.chance_table
		return monster_chances, monster_table

	def gen_monster(self, CR):
		# Roll base stats
		monster = MonsterPart()
		monster.hp = roll(5+CR, CR * 50) + 75
		monster.defense = from_dungeon_level([[roll(CR, CR*2) + CR, 5]], self.dungeon_level) 
		monster.num_die = from_dungeon_level([[int(CR/3) + roll(1, CR), 9]], self.dungeon_level)
		monster.type_die = CR
		monster.mod_die = from_dungeon_level([[roll(1, CR) + CR, 5]], self.dungeon_level)
		monster.xp = CR * 25
		choice1 = self.tier1[random_choice_from_dict(self.tier1_chances)]
		choice2 = self.tier2[random_choice_from_dict(self.tier2_chances)]
		choice3 = self.tier3[random_choice_from_dict(self.tier3_chances)]
		monster.color = choice1.color
		monster.name = ''.join((choice1.name , ' ' , choice2.name , ' ' , choice3.name))
		monster.char = choice2.char
		monster.hp = monster.hp + choice1.hp + choice2.hp + choice3.hp
		monster.defense = monster.defense + choice1.defense + choice2.defense + choice3.defense
		monster.num_die = monster. num_die + choice1.num_die + choice2.num_die + choice3.num_die
		monster.type_die = monster.type_die + choice1.type_die + choice2.type_die + choice3.type_die
		monster.mod_die = monster.mod_die + choice1.mod_die + choice2.mod_die + choice3.mod_die
		monster.xp = monster.xp + choice1.xp + choice2.xp + choice3.xp
		monster.chance_table = choice1.chance_table + choice2.chance_table + choice3.chance_table
		return monster

class MonsterPart:

	def __init__(self, char=None, color=None, name='', hp=0, defense=0, num_die=0, type_die=0, mod_die=0, xp=0, chance_table=0):
		self.char = char
		self.color = color
		self.name = name
		self.hp = hp
		self.defense = defense
		self.num_die = num_die
		self.type_die = type_die
		self.mod_die = mod_die
		self.xp = xp
		self.chance_table = chance_table