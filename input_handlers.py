import tcod as libtcod
from game_states import GameState

def handle_keys(key, game_state):
    if game_state == GameState.PLAYER_TURN:
        return handle_keys_player_turn(key)
    elif game_state == GameState.PLAYER_DEAD:
        return handle_keys_player_dead(key)
    elif game_state in (GameState.SHOW_INVENTORY, GameState.DROP_INVENTORY):
        return handle_keys_show_inventory(key)
    elif game_state == GameState.TARGETING:
        return handle_keys_targeting(key)
    elif game_state == GameState.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameState.CHARACTER_SCREEN:
        return handle_character_screen(key)
    return {}

def handle_keys_player_turn(key):
    key_char = chr(key.c)
    # Movement keys
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}
    # Various keybindings
    if key_char == 'g':
        return {'pickup': True}
    elif key_char == 'i' and key.shift:
        return {'toggle_invis': True}
    elif key_char == 'i':
        return {'show_inventory': True}
    elif key_char == 'd':
        return {'drop_inventory': True}
    elif key_char == '.' and not key.shift:
        return {'wait': True}
    elif key_char == 'e':
        return {'eat': True}
    elif key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ENTER or (key_char == '.'):
        return {'take_stairs': True}
    elif key_char == 'c':
        return {'show_character_screen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_keys_player_dead(key):
    key_char = chr(key.c)
    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}
    return {}

def handle_keys_show_inventory(key):
    index = 0
    if (key.c >= ord('a')) and (key.c <= ord('z')) and key.shift:
        index = key.c - ord('a') + 26
        return {'inventory_index': index}
    elif (key.c >= ord('a')) and (key.c <= ord('z')) and not key.shift:
        index = key.c - ord('a')
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}
    return {}

def handle_keys_targeting(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}

def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_level_up_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'level_up': 'hp'}
    elif key_char == 'b':
        return {'level_up': 'def'}
    elif key_char == 'c':
        return {'level_up': 'str'}
    elif key_char == 'd':
        return {'level_up': 'spd'}
    return {}

def handle_character_screen(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}