import time
import pygame
import gamemode

# Basic game setups
pygame.init()
Clock = pygame.time.Clock()
GameMode = gamemode.GameMode()
GameMode.ResetGame()
pygame.display.update()
ShouldDrawInfo = False
SleepTime = 0.1

while GameMode.GameIsRunning:
    # Event loop
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            GameMode.GameIsRunning = False
        if Event.type == pygame.KEYDOWN:
            if Event.key == pygame.K_s:
                ShouldDrawInfo = not ShouldDrawInfo
            elif Event.key == pygame.K_DOWN:
                SleepTime += 0.01
            elif Event.key == pygame.K_UP:
                SleepTime -= 0.01
                if SleepTime < 0:
                    SleepTime = 0

    # Game loop
    CurrentAliveCharacters = 0
    for i in range(len(GameMode.BlueCharacters)):
        if not GameMode.BlueCharacters[i].IsDead:
            GameMode.BlueCharacters[i].Brain.Think(GameMode.BlueCharacters[i], GameMode)
            GameMode.BlueCharacters[i].React()
            CurrentAliveCharacters += 1
        if not GameMode.RedCharacters[i].IsDead:
            GameMode.RedCharacters[i].Brain.Think(GameMode.RedCharacters[i], GameMode)
            GameMode.RedCharacters[i].React()
            CurrentAliveCharacters += 1
    print("Turn: " + str(GameMode.CurrentTurn) + " | Alive characters: " + CurrentAliveCharacters.__str__())

    if ShouldDrawInfo:
        GameMode.DrawInfo()  # This slow down the game a lot
    time.sleep(SleepTime)

    GameMode.OnTurnEnd()

    # Update loop
    pygame.display.update()
    Clock.tick()
