import math
import random
import pygame
import background
import character


class GameMode:
    number_of_character_each_team = 5
    generations_to_accept_convergence = 10000

    current_generation = 0
    game_is_running = True
    blue_characters = []
    red_characters = []
    blue_characters_locations = []
    red_characters_locations = []
    current_background = None
    number_of_mutations = 0
    current_turn = 0
    best_characters_in_turn = []

    best_fit_ever = -999

    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        self.blue_characters = []
        self.red_characters = []
        self.blue_characters_locations = []
        self.red_characters_locations = []
        self.current_background = None
        self.current_turn = 0

    def reset_game(self):
        if self.current_generation != 0:
            self.get_best_five_characters()
        self.init_new_game()
        self.change_characters_dna()

    def get_best_five_characters(self):
        # Sorting cars by score
        all_characters = self.blue_characters + self.red_characters
        all_characters.sort(key=lambda x: x.rewards, reverse=True)
        self.best_characters_in_turn = all_characters[:5]
        if len(self.best_characters_in_turn) > 0:
            if self.best_characters_in_turn[0].rewards > self.best_fit_ever:
                self.best_fit_ever = self.best_characters_in_turn[0].rewards

    def get_alive_characters(self):
        alive_characters = []
        for current_character in self.blue_characters:
            if not current_character.is_dead:
                alive_characters.append(current_character)
        for current_character in self.red_characters:
            if not current_character.is_dead:
                alive_characters.append(current_character)
        return alive_characters

    def get_alive_characters_by_team(self):
        blue_alive_characters = []
        red_alive_characters = []
        for current_character in self.blue_characters:
            if not current_character.is_dead:
                blue_alive_characters.append(current_character)
        for current_character in self.red_characters:
            if not current_character.is_dead:
                red_alive_characters.append(current_character)
        return blue_alive_characters, red_alive_characters

    def init_new_game(self):
        print("---------- Init generation: " + str(self.current_generation) + " ----------")
        self.reset_variables()
        self.current_background = background.Background()
        self.create_characters()
        self.current_generation += 1

    def generate_random_location(self):
        random_x_loc = random.randrange(0, self.current_background.display_width, 64)
        random_y_loc = random.randrange(0, self.current_background.display_height, 64)
        return random_x_loc, random_y_loc

    def create_characters(self):
        for i in range(self.number_of_character_each_team):
            initial_loc = self.generate_random_location()
            while self.has_character_at_location(initial_loc):
                initial_loc = self.generate_random_location()
            self.blue_characters.append(character.Character(initial_loc, self, True, i))
            self.blue_characters_locations.append(initial_loc)

            initial_loc = self.generate_random_location()
            while self.has_character_at_location(initial_loc):
                initial_loc = self.generate_random_location()
            self.red_characters.append(character.Character(initial_loc, self, False, i))
            self.red_characters_locations.append(initial_loc)

        if self.current_generation == 0:
            self.number_of_mutations = len(self.blue_characters[0].dna)

    def change_characters_dna(self):
        if len(self.best_characters_in_turn) == 0:
            return
        print("Best character score (round): " + str(self.best_characters_in_turn[0].rewards))
        print("Best character DNA(round): " + str(self.best_characters_in_turn[0].dna))
        self.clone_best_characters()
        self.mutate_characters()
        self.number_of_mutations *= 0.999
        if self.number_of_mutations < len(self.blue_characters[0].dna) / 3:
            self.number_of_mutations = len(self.blue_characters[0].dna) / 3
        print("Mutating " + str(math.ceil(self.number_of_mutations)) + " DNAs.")

    def clone_best_characters(self):
        for i in range(len(self.blue_characters)):
            if i >= len(self.best_characters_in_turn):
                break
            self.blue_characters[i].dna = self.best_characters_in_turn[i].dna
            self.red_characters[i].dna = self.best_characters_in_turn[i].dna

    def mutate_characters(self):
        for i in range(len(self.best_characters_in_turn), len(self.blue_characters)):
            self.blue_characters[i].mutate_dna(self.number_of_mutations)
            self.red_characters[i].mutate_dna(self.number_of_mutations)

    def on_turn_end(self):
        if self.check_if_game_over():
            print("Game over in turn: " + str(self.current_turn))
            self.reset_game()
            return
        self.current_turn += 1

    def check_if_game_over(self):
        for current_character in self.blue_characters:
            if current_character.is_dead:
                continue
            return False
        for current_character in self.red_characters:
            if current_character.is_dead:
                continue
            return False
        return True

    def has_character_at_location(self, location, ignored_character=None):
        all_characters = self.get_alive_characters()
        for i in range(len(all_characters)):
            if all_characters[i].current_location == location and all_characters[i] != ignored_character:
                return True
        return False

    def draw_best_fitness(self, initial_x_loc, initial_y_loc, font):
        if self.current_background.screen is None:
            return

        best_fit_text = font.render("Best fitness (round): " + str(self.best_characters_in_turn[0].rewards), True,
                                    (0, 0, 0))
        best_fit_ever_text = font.render("Best fitness (ever): " + str(self.best_fit_ever), True, (0, 0, 0))
        self.current_background.screen.blit(best_fit_ever_text, (initial_x_loc, initial_y_loc))
        self.current_background.screen.blit(best_fit_text, (initial_x_loc, initial_y_loc + 15))

    def draw_current_generation(self, initial_x_loc, initial_y_loc, font):
        current_generation_text = font.render("Generation: " + str(self.current_generation), True, (0, 0, 0))
        self.current_background.screen.blit(current_generation_text, (initial_x_loc, initial_y_loc))

    def draw_neural_net(self, initial_x_loc, initial_y_loc, font):
        bias = 1
        each_neuron_offset = 20
        if self.best_characters_in_turn[0] is None:
            return

        best_character_brain = self.best_characters_in_turn[0].brain

        red_color = (255, 0, 0)
        blue_color = (0, 0, 255)
        neuron_active_color = blue_color if self.best_characters_in_turn[0].blue_team_member else red_color

        self.draw_first_layer_text(initial_x_loc, initial_y_loc, font)

        self.draw_first_layer_neurons(bias, best_character_brain, each_neuron_offset, neuron_active_color,
                                      initial_x_loc,
                                      initial_y_loc)

        self.draw_hidden_layer_neurons(bias, best_character_brain, each_neuron_offset, neuron_active_color,
                                       initial_x_loc,
                                       initial_y_loc)

        self.draw_output_layer_neurons(best_character_brain, each_neuron_offset, neuron_active_color, initial_x_loc,
                                       initial_y_loc)

        self.draw_output_layer_texts(each_neuron_offset, font, initial_x_loc, initial_y_loc)

        self.draw_connections(bias, best_character_brain, each_neuron_offset, neuron_active_color, initial_x_loc,
                              initial_y_loc)

    def draw_connections(self, bias, best_character_brain, each_neuron_offset, neuron_active_color, initial_x_loc,
                         initial_y_loc):
        for i in range(len(best_character_brain.entry_layer.neurons) - bias):
            for j in range(len(best_character_brain.hidden_layers[0].neurons) - bias):
                if best_character_brain.entry_layer.neurons[i].out_value > 0 and \
                        best_character_brain.hidden_layers[0].neurons[
                            j].out_value > 0:
                    pygame.draw.line(self.current_background.screen, neuron_active_color,
                                     (initial_x_loc + 50, initial_y_loc + i * each_neuron_offset),
                                     (initial_x_loc + 100, initial_y_loc + j * each_neuron_offset), 1)
                else:
                    pygame.draw.line(self.current_background.screen, (0, 0, 0),
                                     (initial_x_loc + 50, initial_y_loc + i * each_neuron_offset),
                                     (initial_x_loc + 100, initial_y_loc + j * each_neuron_offset), 1)
        if len(best_character_brain.hidden_layers) > 1:
            for i in range(len(best_character_brain.hidden_layers[0].neurons) - bias):
                for j in range(len(best_character_brain.hidden_layers[1].neurons) - bias):
                    if best_character_brain.hidden_layers[0].neurons[i].out_value > 0:
                        pygame.draw.line(self.current_background.screen, neuron_active_color,
                                         (initial_x_loc + 100, initial_y_loc + i * each_neuron_offset),
                                         (initial_x_loc + 150, initial_y_loc + j * each_neuron_offset), 1)
                    else:
                        pygame.draw.line(self.current_background.screen, (0, 0, 0),
                                         (initial_x_loc + 100, initial_y_loc + i * each_neuron_offset),
                                         (initial_x_loc + 150, initial_y_loc + j * each_neuron_offset), 1)
        for i in range(len(best_character_brain.hidden_layers[-1].neurons) - bias):
            for j in range(len(best_character_brain.last_calculated_output)):
                if best_character_brain.hidden_layers[-1].neurons[i].out_value > 0 and \
                        best_character_brain.last_calculated_output[j] != 0:
                    pygame.draw.line(self.current_background.screen, neuron_active_color,
                                     (initial_x_loc + 100, initial_y_loc + i * each_neuron_offset),
                                     (initial_x_loc + 150, initial_y_loc + j * each_neuron_offset), 1)
                else:
                    pygame.draw.line(self.current_background.screen, (0, 0, 0),
                                     (initial_x_loc + 100, initial_y_loc + i * each_neuron_offset),
                                     (initial_x_loc + 150, initial_y_loc + j * each_neuron_offset), 1)

    def draw_output_layer_texts(self, each_neuron_offset, font, initial_x_loc, initial_y_loc):
        first_neuron_text = font.render("Left", True, (0, 0, 0))
        second_neuron_text = font.render("Right", True, (0, 0, 0))
        third_neuron_text = font.render("Up", True, (0, 0, 0))
        fourth_neuron_text = font.render("Down", True, (0, 0, 0))
        fifth_neuron_text = font.render("Craft", True, (0, 0, 0))
        self.current_background.screen.blit(first_neuron_text, (initial_x_loc + 160, initial_y_loc - 13))
        self.current_background.screen.blit(second_neuron_text,
                                            (initial_x_loc + 160, initial_y_loc + 1 * each_neuron_offset - 13))
        self.current_background.screen.blit(third_neuron_text,
                                            (initial_x_loc + 160, initial_y_loc + 2 * each_neuron_offset - 13))
        self.current_background.screen.blit(fourth_neuron_text,
                                            (initial_x_loc + 160, initial_y_loc + 3 * each_neuron_offset - 13))
        self.current_background.screen.blit(fifth_neuron_text,
                                            (initial_x_loc + 160, initial_y_loc + 4 * each_neuron_offset - 13))

    def draw_output_layer_neurons(self, best_character_brain, each_neuron_offset, neuron_active_color, initial_x_loc,
                                  initial_y_loc):
        for i in range(len(best_character_brain.last_calculated_output)):
            neuron_color = (0, 0, 0) if best_character_brain.last_calculated_output[i] == 0 else neuron_active_color
            pygame.draw.circle(self.current_background.screen, neuron_color,
                               (initial_x_loc + 150, initial_y_loc + i * each_neuron_offset),
                               7)

    def draw_hidden_layer_neurons(self, bias, best_character_brain, each_neuron_offset, neuron_active_color, initial_x_loc,
                                  initial_y_loc):
        for i in range(len(best_character_brain.hidden_layers)):
            for j in range(len(best_character_brain.hidden_layers[i].neurons) - bias):
                neuron_color = (0, 0, 0) if best_character_brain.hidden_layers[i].neurons[
                                               j].out_value == 0 else neuron_active_color
                pygame.draw.circle(self.current_background.screen, neuron_color,
                                   (initial_x_loc + 100 + i * 50, initial_y_loc + j * each_neuron_offset),
                                   7)

    def draw_first_layer_neurons(self, bias, best_character_brain, each_neuron_offset, neuron_active_color, initial_x_loc,
                                 initial_y_loc):
        for i in range(len(best_character_brain.entry_layer.neurons) - bias):
            neuron_color = (0, 0, 0) if best_character_brain.entry_layer.neurons[i].out_value == 0 else neuron_active_color
            pygame.draw.circle(self.current_background.screen, neuron_color,
                               (initial_x_loc + 50, initial_y_loc + i * each_neuron_offset),
                               7)

    def draw_first_layer_text(self, initial_x_loc, initial_y_loc, font):
        first_neuron_text = font.render("LX>0", True, (0, 0, 0))
        second_neuron_text = font.render("LX==0", True, (0, 0, 0))
        third_neuron_text = font.render("LY>0", True, (0, 0, 0))
        fouth_neuron_text = font.render("LY==0", True, (0, 0, 0))
        self.current_background.screen.blit(first_neuron_text, (initial_x_loc, initial_y_loc - 13))
        self.current_background.screen.blit(second_neuron_text, (initial_x_loc, 20 + initial_y_loc - 13))
        self.current_background.screen.blit(third_neuron_text, (initial_x_loc, 40 + initial_y_loc - 13))
        self.current_background.screen.blit(fouth_neuron_text, (initial_x_loc, 60 + initial_y_loc - 13))

    def draw_info(self):
        initial_y_loc = 0
        initial_x_loc = self.current_background.display_width
        pygame.draw.rect(self.current_background.screen, (255, 255, 255), (initial_x_loc, initial_y_loc, 275, 300))

        font = pygame.font.SysFont("comicsansms", 14)
        self.draw_current_generation(initial_x_loc, initial_y_loc, font)
        self.get_best_five_characters()
        self.draw_best_fitness(initial_x_loc, initial_y_loc + 15, font)
        self.draw_neural_net(initial_x_loc, initial_y_loc + 60, font)

    def get_characters_loc(self, blue_team_characters):
        if blue_team_characters:
            return self.blue_characters_locations
        return self.red_characters_locations
