from random import randrange

import pygame.display


class Background:
    rounds_without_spawning_log = 2
    min_rounds_to_spawn_log = 3
    max_rounds_to_spawn_log = 5
    display_width = 1024
    display_height = 1024
    basic_square_size = 64
    screen = None
    square_image_dict = {}
    square_dict = {}
    log_locations = []
    last_gap_location = -1

    grass0_img = pygame.image.load('img/Grass0.png')
    grass1_img = pygame.image.load('img/Grass1.png')
    grass2_img = pygame.image.load('img/Grass2.png')
    grass3_img = pygame.image.load('img/Grass3.png')
    log_img = pygame.image.load('img/Log.png')

    def __init__(self):
        self.screen = pygame.display.set_mode((self.display_width + 275, self.display_height))
        self.reset_background()

    def reset_background(self):
        self.log_locations = []
        self.square_image_dict = {}
        self.square_dict = {}
        self.init_background()

    def init_background(self):
        # filling background with grass
        spawned_at_least_one_log = False
        for current_width in range(0, self.display_width, self.basic_square_size):
            for current_height in range(0, self.display_height, self.basic_square_size):
                random_number = randrange(5)
                if random_number == 1:
                    image_to_use = self.log_img
                    self.log_locations.append((current_width, current_height))
                    self.square_dict[(current_width, current_height)] = "LOG"
                    spawned_at_least_one_log = True
                elif random_number == 2:
                    image_to_use = self.grass1_img
                    self.square_dict[(current_width, current_height)] = "GRASS"
                elif random_number == 3:
                    image_to_use = self.grass2_img
                    self.square_dict[(current_width, current_height)] = "GRASS"
                else:
                    image_to_use = self.grass3_img
                    self.square_dict[(current_width, current_height)] = "GRASS"

                self.screen.blit(image_to_use, (current_width, current_height))
                self.square_image_dict[(current_width, current_height)] = image_to_use
        if not spawned_at_least_one_log:
            self.reset_background()

    def update_square(self, loc, in_type):
        self.square_dict[loc] = in_type
        if in_type == "GRASS":
            self.square_image_dict[loc] = self.grass0_img
        else:
            self.square_image_dict[loc] = self.log_img
