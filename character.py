import math
import random
import time

import pygame
import neuralNetwork
import utils

BASE_REWARD = 100


class Character:
    current_location = (0, 0)
    player_image = None
    game_mode = None
    is_dead = False
    brain = None
    dna = []
    rewards = 0
    has_knife = False
    log_below = False
    blue_team_member = False
    energy = 10
    character_index = -1

    blue_character_with_knife_img = None
    blue_character_img = None
    red_character_with_knife_img = None
    red_character_img = None

    def __init__(self, location, game_mode, blue_team, index):
        self.character_index = index
        self.load_blue_character_images()
        self.load_red_character_images()
        self.current_location = location
        self.game_mode = game_mode
        self.blue_team_member = blue_team
        self.update_image()
        # initializing neural network
        self.brain = neuralNetwork.NeuralNetwork()
        self.dna = []
        for i in range(self.brain.get_weight_amount()):
            self.dna.append((random.randint(0, 20000) / 10.0) - 1000.0)

    def load_blue_character_images(self):
        self.red_character_with_knife_img = pygame.image.load("img/RedCharacterWithKnife.png")
        self.red_character_img = pygame.image.load("img/RedCharacter.png")

    def load_red_character_images(self):
        self.blue_character_with_knife_img = pygame.image.load("img/BlueCharacterWithKnife.png")
        self.blue_character_img = pygame.image.load("img/BlueCharacter.png")

    def update_image(self):
        if self.game_mode is None:
            return
        if self.game_mode.current_background is None:
            return

        if self.is_dead:
            image_below = self.game_mode.current_background.square_image_dict[self.current_location]
            self.game_mode.current_background.screen.blit(image_below, self.current_location)
            return

        if self.has_knife:
            if self.blue_team_member:
                self.player_image = self.blue_character_with_knife_img
            else:
                self.player_image = self.red_character_with_knife_img
        else:
            if self.blue_team_member:
                self.player_image = self.blue_character_img
            else:
                self.player_image = self.red_character_img

        # Updating location
        image_below = self.game_mode.current_background.square_image_dict[self.current_location]
        self.game_mode.current_background.screen.blit(image_below, self.current_location)
        self.game_mode.current_background.screen.blit(self.player_image, self.current_location)

    def react(self):
        output_len = len(self.brain.last_calculated_output)
        for i in range(output_len):
            if self.brain.last_calculated_output[i] > 0:
                self.do_action(i)
                return
        self.do_action(-1)

    def move_left(self):
        self.move((-64, 0))

    def move_right(self):
        self.move((64, 0))

    def move_up(self):
        self.move((0, -64))

    def move_down(self):
        self.move((0, 64))

    def move(self, position):
        if self.game_mode.current_background is None:
            return

        location_to_go = (self.current_location[0] + position[0], self.current_location[1] + position[1])
        if location_to_go[0] < 0 or location_to_go[0] >= self.game_mode.current_background.display_width or \
                location_to_go[1] < 0 or location_to_go[1] >= self.game_mode.current_background.display_height \
                or self.game_mode.has_character_at_location(location_to_go):
            return

        image_below = self.game_mode.current_background.square_image_dict[self.current_location]
        self.game_mode.current_background.screen.blit(image_below, self.current_location)
        self.current_location = location_to_go
        self.game_mode.current_background.screen.blit(self.player_image, self.current_location)
        if self.blue_team_member:
            self.game_mode.blue_characters_locations[self.character_index] = self.current_location
        else:
            self.game_mode.red_characters_locations[self.character_index] = self.current_location


    def die(self):
        self.is_dead = True
        self.update_image()

    def mutate_dna(self, number_of_mutations):
        for k in range(math.ceil(number_of_mutations)):
            in_type = random.randint(0, 2)
            index = random.randint(0, len(self.dna) - 1)
            if in_type == 0:
                self.dna[index] = (random.randint(0, 20000) / 10.0) - 1000.0
            elif in_type == 1:
                number = (random.randint(0, 10000) / 10000.0) + 0.5
                self.dna[index] *= self.dna[index] * number
            elif in_type == 2:
                number = (random.randint(0, 20000) / 10.0) - 1000.0 / 100.0
                self.dna[index] += self.dna[index] + number

    def check_should_die(self):
        if self.energy == 0:
            self.die()

    def do_action(self, action_index):
        self.energy -= 1
        if action_index == 0:
            self.move_left()
        elif action_index == 1:
            self.move_right()
        elif action_index == 2:
            self.move_up()
        elif action_index == 3:
            self.move_down()
        elif action_index == 4:
            self.craft_knife()
        elif action_index == 5:
            self.kill_enemy()
        else:
            self.game_mode.current_background.screen.blit(self.player_image, self.current_location)  # Do nothing
        self.check_should_die()

    def craft_knife(self):
        if self.game_mode.current_background is None:
            return

        if self.game_mode.current_background.square_dict[self.current_location] != "LOG" or \
                self.has_knife:
            return

        self.rewards += 10

        self.game_mode.current_background.update_square(self.current_location, "GRASS")
        self.game_mode.current_background.log_locations.remove(self.current_location)
        self.has_knife = True
        self.update_image()

    def get_closest_enemy_index(self, enemies_loc, enemies):
        closest_dist = 99999
        closest_enemy_index = -1

        for i in range(len(enemies_loc)):
            if enemies[i].is_dead:
                continue

            current_dist = utils.distance_between_locations(enemies_loc[i], self.current_location)
            if closest_dist > current_dist:
                closest_dist = current_dist
                closest_enemy_index = i

        found_loc = enemies_loc[closest_enemy_index]
        found_dist = found_loc[0] - self.current_location[0], found_loc[1] - self.current_location[
            1]

        if abs(found_dist[0]) > 64 or abs(found_dist[1]) > 64 or abs(found_dist[0]) == 64 and abs(found_dist[1]) == 64:
            return -1

        return closest_enemy_index

    def kill_enemy(self):
        if not self.has_knife:
            return

        enemies = self.game_mode.red_characters if self.blue_team_member else self.game_mode.blue_characters
        closest_enemy_index = self.get_closest_enemy_index(self.game_mode.get_characters_loc(not self.blue_team_member), enemies)
        if closest_enemy_index == -1:
            print("Trying to kill enemy, has knife but has no close enemy.")
            return

        enemies[closest_enemy_index].die()
        self.rewards += 50
