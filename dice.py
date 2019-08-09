from random import randint

def roll(number, sides):
	total = 0

	for i in range(number):
		total += randint(1, sides)

	return total
