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
