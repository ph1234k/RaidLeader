import tcod as libtcod
from game_messages import Message

def heal(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')

	results = []

	if entity.fighter.hp == entity.fighter.max_hp:
		results.append({'consumed': False, 'message': Message('You are already at full health!', libtcod.yellow)})
	else:
		# Time to heal, taking negative damage heals and our take_damage
		#  already cheacks and corrects for health changes. 
		entity.fighter.take_damage(amount*-1)
		results.append({'consumed': True, 'message':Message('Your wounds start to feel better!', libtcod.green)})

	return results

def cast_lightning(*args, **kwargs):
	caster = args[0]
	maximum_range = kwargs.get('maximum_range')
	damage = kwargs.get('damage')
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')

	results = []

	target = None
	closest_distance = maximum_range + 1

	for entity in entities:
		if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
			distance = caster.distance_to(entity)

			if distance < closest_distance:
				target = entity
				closest_distance = distance

	if target:
		results.append({'consumed': True, 'target': target, 'message': Message('A bolt of lighting strikes the {0} dealing {1} damage!'.format(target.name, damage))})
		results.extend(target.fighter.take_damage(damage))
	else:
		results.append({'consumed': False, 'target': None, 'message': Message("No enemy is in range of spell.", libtcod.red)})

	return results