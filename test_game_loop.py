import pygame
import character
import gameLoops
import gamemode


class TestGameLoop:
    mocked_game_mode = gamemode.GameMode()

    def test_event_loop_positive_time_to_sleep(self):
        current_time_to_sleep = 0
        mocked_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN})
        returned_time_to_sleep, not_used_draw_info = gameLoops.run_event_loop(current_time_to_sleep, True, [mocked_event], self.mocked_game_mode)
        assert returned_time_to_sleep > current_time_to_sleep

    def test_event_loop_negative_time_to_sleep(self):
        current_time_to_sleep = 0
        mocked_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP})
        returned_time_to_sleep, not_used_draw_info = gameLoops.run_event_loop(current_time_to_sleep, True, [mocked_event], self.mocked_game_mode)
        assert returned_time_to_sleep > current_time_to_sleep

    def test_event_loop_quit(self):
        mocked_event = pygame.event.Event(pygame.QUIT, {"key": pygame.K_ESCAPE})
        not_used_time_to_sleep, not_used_draw_info = gameLoops.run_event_loop(0, True, [mocked_event], self.mocked_game_mode)
        assert self.mocked_game_mode.game_is_running is False

    def test_game_loop_no_characters(self):
        self.mocked_game_mode.reset_variables()
        gameLoops.run_game_loop(self.mocked_game_mode)

    def test_game_loop_no_blue_characters(self):
        self.mocked_game_mode.reset_variables()
        self.mocked_game_mode.red_characters = [character.Character((0, 0), self.mocked_game_mode, False)]
        gameLoops.run_game_loop(self.mocked_game_mode)

    def test_game_loop_no_red_characters(self):
        self.mocked_game_mode.reset_variables()
        self.mocked_game_mode.blue_characters = [character.Character((0, 0), self.mocked_game_mode, True)]
        gameLoops.run_game_loop(self.mocked_game_mode)

    def test_game_loop_blue_characters_dead(self):
        self.mocked_game_mode.reset_variables()
        self.mocked_game_mode.blue_characters = [character.Character((0, 0), self.mocked_game_mode, True)]
        self.mocked_game_mode.blue_characters[0].die()
        self.mocked_game_mode.red_characters = [character.Character((0, 0), self.mocked_game_mode, False)]
        gameLoops.run_game_loop(self.mocked_game_mode)

    def test_game_loop_red_characters_dead(self):
        self.mocked_game_mode.reset_variables()
        self.mocked_game_mode.blue_characters = [character.Character((0, 0), self.mocked_game_mode, True)]
        self.mocked_game_mode.red_characters = [character.Character((0, 0), self.mocked_game_mode, False)]
        self.mocked_game_mode.red_characters[0].die()
        gameLoops.run_game_loop(self.mocked_game_mode)


