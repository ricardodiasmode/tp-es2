from random import randrange

import pygame.display


class Background:
    display_width = 1024
    debug_width = 275
    display_height = 1024
    basic_square_size = 64
    screen = None

    square_image_dict = {}
    square_dict = {}
    log_locations = []

    grass0_img = None
    grass1_img = None
    grass2_img = None
    grass3_img = None
    log_img = None

    def __init__(self):
        self.load_grass_images()
        self.load_log_image()
        self.screen = pygame.display.set_mode((self.display_width + self.debug_width, self.display_height))
        self.reset_background()

    def load_grass_images(self):
        self.grass0_img = pygame.image.load('img/Grass0.png')
        self.grass1_img = pygame.image.load('img/Grass1.png')
        self.grass2_img = pygame.image.load('img/Grass2.png')
        self.grass3_img = pygame.image.load('img/Grass3.png')

    def load_log_image(self):
        self.log_img = pygame.image.load('img/Log.png')

    def reset_background(self):
        self.reset_variables()
        self.init_background()

    def reset_variables(self):
        self.log_locations = []
        self.square_image_dict = {}
        self.square_dict = {}

    def init_background(self):
        for current_width in range(0, self.display_width, self.basic_square_size):
            for current_height in range(0, self.display_height, self.basic_square_size):
                current_location = (current_width, current_height)
                if self.square_dict.get(current_location) is not None:
                    continue

                random_number = randrange(5)
                if random_number == 1:
                    image_to_use = self.log_img
                    if current_location not in self.log_locations:
                        self.log_locations.append(current_location)
                    self.square_dict.update({current_location: "LOG"})
                elif random_number == 2:
                    image_to_use = self.grass1_img
                    self.square_dict.update({current_location: "GRASS"})
                elif random_number == 3:
                    image_to_use = self.grass2_img
                    self.square_dict.update({current_location: "GRASS"})
                else:
                    image_to_use = self.grass3_img
                    self.square_dict.update({current_location: "GRASS"})

                self.screen.blit(image_to_use, current_location)
                self.square_image_dict[current_location] = image_to_use
        if not self.log_locations:
            self.reset_background()

    def update_square(self, loc, in_type):
        self.square_dict[loc] = in_type
        if in_type == "GRASS":
            self.square_image_dict[loc] = self.grass0_img
        else:
            self.square_image_dict[loc] = self.log_img
