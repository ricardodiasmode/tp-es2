import math


def get_closest_log_dist(character_loc, background):
    if background is None:
        return 0, 0

    closest_log_index = 0
    closest_dist = 999999
    for i in range(len(background.log_locations)):
        if closest_dist > distance_between_locations(background.log_locations[i], character_loc):
            closest_dist = distance_between_locations(background.log_locations[i], character_loc)
            closest_log_index = i
    found_loc = background.log_locations[closest_log_index]
    return found_loc[0] - character_loc[0], found_loc[1] - character_loc[1]


def distance_between_locations(first_loc, second_loc):
    return math.sqrt((first_loc[0] - second_loc[0]) ** 2 + (
            first_loc[1] - second_loc[1]) ** 2)


def get_closest_enemy_dist(current_character, current_game_mode):
    if current_game_mode is None:
        return 0, 0

    closest_enemy_index = -1
    closest_dist = 999999

    enemies = current_game_mode.red_characters if current_character.blue_team_member else current_game_mode.blue_characters

    for i in range(len(enemies)):
        current_dist = distance_between_locations(enemies[i].current_location, current_character.current_location)
        if closest_dist > current_dist:
            closest_dist = current_dist
            closest_enemy_index = i

    if closest_enemy_index == -1:
        return 0, 0

    found_loc = enemies[closest_enemy_index].current_location
    return found_loc[0] - current_character.current_location[0], found_loc[1] - current_character.current_location[1]