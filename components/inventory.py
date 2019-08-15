import tcod as libtcod
from game_messages import Message

class  Inventory:
	def __init__(self, capacity):
		self.capacity = capacity
		self.items = []
	
	def add_item(self, item):
		results = []

		if len(self.items) >= self.capacity:
			results.append({
				'item_added': None,
				'message': Message('You cannot carry anymore. Your inventory is full.', libtcod.yellow)
				})
		else:
			results.append({
				'item_added': item,
				'message': Message('You pick up the {0}'.format(item.name), libtcod.blue)
				})
			self.items.append(item)
		return results

	def use(self, item_entity, **kwargs):
		results = []

		item_component = item_entity.item

		if item_component.use_function is None:
			if item_entity.equippable is None:
				results.append({'message': Message('{0} is not usable...'.format(item_entity.name), libtcod.yellow)})
			else:
				results.append({'equip': item_entity})
		else:
			if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
				results.append({'targeting': item_entity})
			else:
				kwargs = {**item_component.function_kwargs, **kwargs}
				item_use_results = item_component.use_function(self.owner, **kwargs)

				for item_use_result in item_use_results:
					if item_use_result.get('consumed'):
						self.remove_item(item_entity)
				results.extend(item_use_results)
		return results

	def remove_item(self, item):
		self.items.remove(item)

	def drop_item(self, item):
		results = []
		if self.owner.equipment.weapon == item or self.owner.equipment.head == item or self.owner.equipment.neck == item or self.owner.equipment.chest == item or self.owner.equipment.gloves == item or self.owner.equipment.legs == item or self.owner.equipment.boots == item or self.owner.equipment.left_ring == item or self.owner.equipment.right_ring == item:
			self.owner.equipment.toggle_equip(item)
		item.x = self.owner.x
		item.y = self.owner.y

		self.remove_item(item)
		results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name), libtcod.yellow)})

		return results