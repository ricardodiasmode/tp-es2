import time
import pygame
import gamemode
import gameLoops


class GameInitializer:
    clock = None
    game_mode = None
    should_draw_info = False
    sleep_time = 0.0

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.game_mode = gamemode.GameMode()
        self.game_mode.reset_game()
        pygame.display.update()

    def start_game_loop(self):
        while self.game_mode.game_is_running:
            self.run_turn()

    def run_turn(self):
        self.should_draw_info, self.sleep_time = gameLoops.run_event_loop(self.sleep_time, self.should_draw_info,
                                                                          pygame.event.get(), self.game_mode)
        gameLoops.run_game_loop(self.game_mode)

        if self.should_draw_info:
            self.game_mode.draw_info()

        time.sleep(self.sleep_time)

        self.game_mode.on_turn_end()

        pygame.display.update()
        self.clock.tick()
