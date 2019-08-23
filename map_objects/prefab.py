import tcod as libtcod

from map_objects.rectangle import Rect
from dice import roll

class Prefab(Rect):
	'''
	WARNING: Prefab cells[0][*] and [*][0] are NOT actually drawn 
	'''
	def __init__(self, x, y, w, h):
		super(Prefab, self).__init__(x, y, w, h)
		self.cells = [[0 for y in range(h)] for x in range(w)]

class PFRoom(Prefab):
	def __init__(self, x, y):
		w = 10 + 2
		h = 10 + 2
		super(PFRoom, self).__init__(x, y, w, h)
		self.cells[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.cells[1] = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
		self.cells[2] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
		self.cells[3] = [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0]
		self.cells[4] = [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
		self.cells[5] = [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
		self.cells[6] = [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
		self.cells[7] = [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
		self.cells[8] = [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0]
		self.cells[9] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
		self.cells[10] = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
		self.cells[11] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

class PFDiningHall(Prefab):
	def __init__(self, x, y):
		if roll(1, 2) == 1:
			w = 6
			h = 20
		else:
			w = 20
			h = 6
		super(PFDiningHall, self).__init__(x, y, w, h)
		if w > h:
			self.cells[0] = [0,1,1,1,1,0]
			self.cells[1] = [0,1,1,1,1,0]
			self.cells[2] = [0,1,1,1,1,0]
			self.cells[3] = [0,1,1,1,1,0]
			self.cells[4] = [0,1,1,1,1,0]
			self.cells[5] = [0,1,1,1,1,0]
			self.cells[6] = [0,1,1,1,1,0]
			self.cells[7] = [0,1,1,1,1,0]
			self.cells[8] = [0,1,1,1,1,0]
			self.cells[9] = [0,1,1,1,1,0]
			self.cells[10] = [0,1,1,1,1,0]
			self.cells[11] = [0,1,1,1,1,0]
			self.cells[12] = [0,1,1,1,1,0]
			self.cells[13] = [0,1,1,1,1,0]
			self.cells[14] = [0,1,1,1,1,0]
			self.cells[15] = [0,1,1,1,1,0]
			self.cells[16] = [0,1,1,1,1,0]
			self.cells[17] = [0,1,1,1,1,0]
			self.cells[18] = [0,1,1,1,1,0]
			self.cells[19] = [0,1,1,1,1,0]
		else:
			self.cells[0] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			self.cells[1] = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
			self.cells[2] = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
			self.cells[3] = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
			self.cells[4] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
