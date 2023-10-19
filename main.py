import time
import pygame
import gamemode


def RunEventLoop(TimeToSleep, DrawInfo):
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            GameMode.GameIsRunning = False
        if Event.type == pygame.KEYDOWN:
            if Event.key == pygame.K_s:
                DrawInfo = not DrawInfo
            elif Event.key == pygame.K_DOWN:
                TimeToSleep += 0.01
            elif Event.key == pygame.K_UP:
                TimeToSleep -= 0.01
                if TimeToSleep < 0:
                    TimeToSleep = 0
    return DrawInfo, TimeToSleep


def RunGameLoop():
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


# Basic game setups
pygame.init()
Clock = pygame.time.Clock()
GameMode = gamemode.GameMode()
GameMode.ResetGame()
pygame.display.update()
ShouldDrawInfo = False
SleepTime = 0.0

while GameMode.GameIsRunning:
    ShouldDrawInfo, SleepTime = RunEventLoop(SleepTime, ShouldDrawInfo)
    RunGameLoop()

    if ShouldDrawInfo:
        GameMode.DrawInfo()  # This slow down the game a lot

    time.sleep(SleepTime)

    GameMode.OnTurnEnd()

    pygame.display.update()
    Clock.tick()
