import time
import pygame
import gamemode


def run_event_loop(time_to_sleep, draw_info):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_mode.game_is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                draw_info = not draw_info
            elif event.key == pygame.K_DOWN:
                time_to_sleep += 0.01
            elif event.key == pygame.K_UP:
                time_to_sleep -= 0.01
                if time_to_sleep < 0:
                    time_to_sleep = 0
    return draw_info, time_to_sleep


def run_game_loop():
    current_alive_characters = 0
    for i in range(len(game_mode.blue_characters)):
        if not game_mode.blue_characters[i].is_dead:
            game_mode.blue_characters[i].brain.Think(game_mode.blue_characters[i], game_mode)
            game_mode.blue_characters[i].React()
            current_alive_characters += 1
        if not game_mode.red_characters[i].is_dead:
            game_mode.red_characters[i].brain.Think(game_mode.red_characters[i], game_mode)
            game_mode.red_characters[i].React()
            current_alive_characters += 1
    print("Turn: " + str(game_mode.current_turn) + " | Alive characters: " + current_alive_characters.__str__())


# Basic game setups
pygame.init()
clock = pygame.time.Clock()
game_mode = gamemode.GameMode()
game_mode.reset_game()
pygame.display.update()
should_draw_info = False
sleep_time = 0.0

while game_mode.game_is_running:
    should_draw_info, sleep_time = run_event_loop(sleep_time, should_draw_info)
    run_game_loop()

    if should_draw_info:
        game_mode.draw_info()  # This slow down the game a lot

    time.sleep(sleep_time)

    game_mode.on_turn_end()

    pygame.display.update()
    clock.tick()
