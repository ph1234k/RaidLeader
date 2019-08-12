from dice import roll, random_choice_from_dict

def gen_monster_table(game_map, constants):
	# Returns two dcitionaries
	# One is a lookup of weights for use in random_choice_from_dict
	# The other contains the data needed to place each monster