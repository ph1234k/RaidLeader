# Skeleton for some RL games

## Goals

1. A playable engine
2. Simple to add, remove and adjust entities
3. Simple to adjust to novel mechanics

## Compatability notes

Developed in Python 3.7.
Requires tcod (libtcod) as dependency.
May add in Numpy in the future -  currently not depend.

## Play/Testing notes
To play, ensure you have a compatible version of python installed.
Make sure to install libtcod as well.

Then run `py engine.py` to start. 

You can use the arrow keys or VIM keys to move around. 
"i" for inventory
"d" for dropping an item
"g" for picking up an item
"e" for eating corpses
"." to wait
"c" for character screen
"ESC" to save and quit
To use an item, open the inventory and then press the appropraite key that represents the item you wish to use. 