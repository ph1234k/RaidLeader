import tcod as libtcod
from game_messages import Message
from components.ai import ConfusedMonster

def heal(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')

	results = []

	if entity.fighter.hp == entity.fighter.max_hp:
		results.append({'consumed': False, 'message': Message('You are already at full health!', libtcod.yellow)})
	else:
		# Time to heal, taking negative damage heals and our take_damage
		#  already checks and corrects for health changes. 
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

def cast_fireball(*args, **kwargs):
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage')
	radius = kwargs.get('radius')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')

	results = []

	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({'consumed': False ,'message': Message("Cannot target a tile that is not in range.", libtcod.yellow)})
		return results

	results.append({'consumed': True, 'message': Message('The fireball explodes, hitting everything within {0} tiles!'.format(radius), libtcod.orange)})

	for entity in entities:
		if entity.distance(target_x, target_y) <= radius and entity.fighter:
			results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage), libtcod.orange)})
			results.extend(entity.fighter.take_damage(damage))

	return results

def cast_confuse(*args, **kwargs):
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')

	results = []

	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({'consumed': False, 'message': Message('You cannot target a tile outside of your field of view.', libtcod.yellow)})
		return results

	for entity in entities:
		if entity.x == target_x and entity.y == target_y and entity.ai:
			entity.ai = ConfusedMonster(entity.ai, 10)
			entity.ai.owner = entity

			results.append({'consumed': True, 'message': Message('The eyes of the {} glaze over. It starts to stumble around!'.format(entity.name), libtcod.light_green)})

			break
	else:
		results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

	return results