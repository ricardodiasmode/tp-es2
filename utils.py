import math

import gamemode


def GetClosestLogDist(character_loc, background):
    closest_log_index = 0
    closest_dist = 999999
    for i in range(len(background.LogLocations)):
        if closest_dist > DistanceBetweenLocations(background.LogLocations[i], character_loc):
            closest_dist = DistanceBetweenLocations(background.LogLocations[i], character_loc)
            closest_log_index = i
    return background.LogLocations[closest_log_index]


def GetClosestEnemyDist(character_loc, character_is_blue, game_mode):
    closest_enemy_index = 0
    closest_dist = 999999
    if character_is_blue:
        enemies = game_mode.BlueCharacters
    else:
        enemies = game_mode.RedCharacters

    for i in range(len(enemies)):
        if closest_dist > DistanceBetweenLocations(enemies[i].CurrentLocation, character_loc):
            closest_dist = DistanceBetweenLocations(enemies[i].CurrentLocation, character_loc)
            closest_enemy_index = i
    return enemies[closest_enemy_index].CurrentLocation


def DistanceBetweenLocations(first_loc, second_loc):
    return math.sqrt((first_loc[0] - second_loc[0]) ** 2 + (
            first_loc[1] - second_loc[1]) ** 2)
