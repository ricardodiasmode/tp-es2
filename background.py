from random import randrange

import pygame.display


class Background:
    RoundsWithoutSpawningLog = 2
    MinRoundsToSpawnLog = 3
    MaxRoundsToSpawnLog = 5
    DisplayWidth = 1024
    DisplayHeight = 1024
    BasicSquareSize = 64
    Screen = None
    SquareImageDict = {}
    SquareDict = {}
    LogLocations = []
    LastGapLocation = -1

    Grass0Img = pygame.image.load('img/Grass0.png')
    Grass1Img = pygame.image.load('img/Grass1.png')
    Grass2Img = pygame.image.load('img/Grass2.png')
    Grass3Img = pygame.image.load('img/Grass3.png')
    LogImg = pygame.image.load('img/Log.png')

    def __init__(self):
        self.Screen = pygame.display.set_mode((self.DisplayWidth + 275, self.DisplayHeight))
        self.ResetBackground()

    def ResetBackground(self):
        self.LogLocations = []
        self.SquareImageDict = {}
        self.SquareDict = {}
        self.InitBackground()

    def InitBackground(self):
        # filling background with grass
        spawned_at_least_one_log = False
        for currentWidth in range(0, self.DisplayWidth, self.BasicSquareSize):
            for currentHeight in range(0, self.DisplayHeight, self.BasicSquareSize):
                randomNumber = randrange(5)
                ImageToUse = self.Grass0Img
                if randomNumber == 1:
                    ImageToUse = self.LogImg
                    self.LogLocations.append((currentWidth, currentHeight))
                    self.SquareDict[(currentWidth, currentHeight)] = "LOG"
                    spawned_at_least_one_log = True
                elif randomNumber == 2:
                    ImageToUse = self.Grass1Img
                    self.SquareDict[(currentWidth, currentHeight)] = "GRASS"
                elif randomNumber == 3:
                    ImageToUse = self.Grass2Img
                    self.SquareDict[(currentWidth, currentHeight)] = "GRASS"
                else:
                    ImageToUse = self.Grass3Img
                    self.SquareDict[(currentWidth, currentHeight)] = "GRASS"

                self.Screen.blit(ImageToUse, (currentWidth, currentHeight))
                self.SquareImageDict[(currentWidth, currentHeight)] = ImageToUse
        if not spawned_at_least_one_log:
            self.ResetBackground()
