import math
import random
import pygame
import background
import character
import utils


class GameMode:
    NumberOfCharacterEachTeam = 10
    GenerationsToAcceptConvergence = 10000

    CurrentGeneration = 0
    GameIsRunning = True
    BlueCharacters = []
    RedCharacters = []
    CurrentBackground = None
    NumberOfMutations = 0
    CurrentTurn = 0
    BestCharactersInTurn = []

    BestFitEver = -999

    def __init__(self):
        self.ResetVariables()

    def ResetVariables(self):
        self.BlueCharacters = []
        self.RedCharacters = []
        self.CurrentBackground = None
        self.CurrentTurn = 0

    def ResetGame(self):
        if self.CurrentGeneration != 0:
            self.GetBestFiveCharacters()
        self.InitNewGame()
        self.ChangeCharactersDna()

    def GetBestFiveCharacters(self):
        # Sorting cars by score
        AllCharacters = self.BlueCharacters + self.RedCharacters
        AllCharacters.sort(key=lambda x: x.Rewards, reverse=True)
        self.BestCharactersInTurn = AllCharacters[:5]
        if len(self.BestCharactersInTurn) > 0:
            if self.BestCharactersInTurn[0].Rewards > self.BestFitEver:
                self.BestFitEver = self.BestCharactersInTurn[0].Rewards

    def GetAliveCharacters(self):
        AliveCharacters = []
        for CurrentCharacter in self.BlueCharacters:
            if not CurrentCharacter.IsDead:
                AliveCharacters.append(CurrentCharacter)
        for CurrentCharacter in self.RedCharacters:
            if not CurrentCharacter.IsDead:
                AliveCharacters.append(CurrentCharacter)
        return AliveCharacters

    def GetAliveCharactersByTeam(self):
        BlueAliveCharacters = []
        RedAliveCharacters = []
        for CurrentCharacter in self.BlueCharacters:
            if not CurrentCharacter.IsDead:
                BlueAliveCharacters.append(CurrentCharacter)
        for CurrentCharacter in self.RedCharacters:
            if not CurrentCharacter.IsDead:
                RedAliveCharacters.append(CurrentCharacter)
        return BlueAliveCharacters, RedAliveCharacters

    def InitNewGame(self):
        print("---------- Init generation: " + str(self.CurrentGeneration) + " ----------")
        self.ResetVariables()
        self.CurrentBackground = background.Background()
        self.CreateCharacters()
        self.CurrentGeneration += 1

    def GenerateRandomLocation(self):
        RandomXLoc = random.randrange(0, self.CurrentBackground.DisplayWidth, 64)
        RandomYLoc = random.randrange(0, self.CurrentBackground.DisplayHeight, 64)
        return (RandomXLoc, RandomYLoc)

    def CreateCharacters(self):
        for i in range(self.NumberOfCharacterEachTeam):
            InitialLoc = self.GenerateRandomLocation()
            while self.HasCharacterAtLocation(InitialLoc):
                InitialLoc = self.GenerateRandomLocation()
            self.BlueCharacters.append(character.Character(InitialLoc, self, True))

            InitialLoc = self.GenerateRandomLocation()
            while self.HasCharacterAtLocation(InitialLoc):
                InitialLoc = self.GenerateRandomLocation()
            self.RedCharacters.append(character.Character(InitialLoc, self, False))

        if self.CurrentGeneration == 0:
            self.NumberOfMutations = len(self.BlueCharacters[0].Dna)

    def ChangeCharactersDna(self):
        if len(self.BestCharactersInTurn) == 0:
            return
        print("Best character score (round): " + str(self.BestCharactersInTurn[0].Rewards))
        print("Best character DNA(round): " + str(self.BestCharactersInTurn[0].Dna))
        self.CloneBestCharacters()
        self.MutateCharacters()
        self.NumberOfMutations *= 0.999
        if self.NumberOfMutations < len(self.BlueCharacters[0].Dna) / 3:
            self.NumberOfMutations = len(self.BlueCharacters[0].Dna) / 3
        print("Mutating " + str(math.ceil(self.NumberOfMutations)) + " DNAs.")

    def CloneBestCharacters(self):
        for i in range(len(self.BlueCharacters)):
            if i < len(self.BestCharactersInTurn):
                self.BlueCharacters[i].Dna = self.BestCharactersInTurn[i].Dna
                self.RedCharacters[i].Dna = self.BestCharactersInTurn[i].Dna

    def MutateCharacters(self):
        for i in range(len(self.BestCharactersInTurn), len(self.BlueCharacters)):
            self.BlueCharacters[i].MutateDna(self.NumberOfMutations)
            self.RedCharacters[i].MutateDna(self.NumberOfMutations)

    def OnTurnEnd(self):
        if self.CheckIfGameOver():
            print("Game over in turn: " + str(self.CurrentTurn))
            self.ResetGame()
            return
        self.CurrentTurn += 1

    def CheckIfGameOver(self):
        for CurrentCharacter in self.BlueCharacters:
            if CurrentCharacter.IsDead:
                continue
            return False
        for CurrentCharacter in self.RedCharacters:
            if CurrentCharacter.IsDead:
                continue
            return False
        return True

    def HasCharacterAtLocation(self, Location, IgnoredCharacter = None):
        AllCharacters = self.GetAliveCharacters()
        for i in range(len(AllCharacters)):
            if AllCharacters[i].CurrentLocation == Location and AllCharacters[i] != IgnoredCharacter:
                return True
        return False

    def GetCharacterClose(self, IgnoredCharacter):
        AllCharacters = self.GetAliveCharacters()
        AllCharacters.remove(IgnoredCharacter)

        ClosestDist, Enemy = utils.GetClosestEnemyDist(IgnoredCharacter.CurrentLocation, IgnoredCharacter.BlueTeamMember, self)
        if (ClosestDist[0] == 0 and abs(ClosestDist[1]) == 64 or
            ClosestDist[0] == 64 and abs(ClosestDist[1]) == 0) and Enemy is not None:
            return Enemy

        return None

    def DrawBestFitness(self, initial_x_loc, initial_y_loc):
        if self.CurrentBackground.Screen is None:
            return

        Font = pygame.font.SysFont("comicsansms", 13)
        BestFitText = Font.render("Best fitness (round): " + str(self.BestCharactersInTurn[0].Rewards), True, (0, 0, 0))
        BestFitEverText = Font.render("Best fitness (ever): " + str(self.BestFitEver), True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(BestFitEverText, (initial_x_loc, initial_y_loc))
        self.CurrentBackground.Screen.blit(BestFitText, (initial_x_loc, initial_y_loc + 15))

    def DrawCurrentGeneration(self, initial_x_loc, initial_y_loc):
        Font = pygame.font.SysFont("comicsansms", 14)
        CurrentGenerationText = Font.render("Generation: " + str(self.CurrentGeneration), True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(CurrentGenerationText, (initial_x_loc, initial_y_loc))

    def DrawNeuralNet(self, initial_x_loc, initial_y_loc):
        BIAS = 1
        EachNeuronOffset = 20
        if self.BestCharactersInTurn[0] is None:
            return

        BestCharacterBrain = self.BestCharactersInTurn[0].Brain

        RedColor = (255, 0, 0)
        BlueColor = (0, 0, 255)
        NeuronActiveColor = BlueColor if self.BestCharactersInTurn[0].BlueTeamMember else RedColor

        # Drawing first layer texts
        Font = pygame.font.SysFont("comicsansms", 14)
        FirstNeuronText = Font.render("LX>0", True, (0, 0, 0))
        SecondNeuronText = Font.render("LX==0", True, (0, 0, 0))
        ThirdNeuronText = Font.render("LY>0", True, (0, 0, 0))
        FouthNeuronText = Font.render("LY==0", True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(FirstNeuronText, (initial_x_loc, initial_y_loc - 13))
        self.CurrentBackground.Screen.blit(SecondNeuronText, (initial_x_loc, 20 + initial_y_loc - 13))
        self.CurrentBackground.Screen.blit(ThirdNeuronText, (initial_x_loc, 40 + initial_y_loc - 13))
        self.CurrentBackground.Screen.blit(FouthNeuronText, (initial_x_loc, 60 + initial_y_loc - 13))

        # Drawing first layer neurons
        for i in range(len(BestCharacterBrain.EntryLayer.Neurons) - BIAS):
            NeuronColor = (0, 0, 0) if BestCharacterBrain.EntryLayer.Neurons[i].OutValue == 0 else NeuronActiveColor
            pygame.draw.circle(self.CurrentBackground.Screen, NeuronColor,
                               (initial_x_loc + 50, initial_y_loc + i * EachNeuronOffset),
                               7)

        # Drawing hidden layers neurons
        for i in range(len(BestCharacterBrain.HiddenLayers)):
            for j in range(len(BestCharacterBrain.HiddenLayers[i].Neurons) - BIAS):
                NeuronColor = (0, 0, 0) if BestCharacterBrain.HiddenLayers[i].Neurons[j].OutValue == 0 else NeuronActiveColor
                pygame.draw.circle(self.CurrentBackground.Screen, NeuronColor,
                                   (initial_x_loc + 100 + i * 50, initial_y_loc + j * EachNeuronOffset),
                                   7)

        # Drawing output layer neurons
        for i in range(len(BestCharacterBrain.LastCalculatedOutput)):
            NeuronColor = (0, 0, 0) if BestCharacterBrain.LastCalculatedOutput[i] == 0 else NeuronActiveColor
            pygame.draw.circle(self.CurrentBackground.Screen, NeuronColor,
                               (initial_x_loc + 150, initial_y_loc + i * EachNeuronOffset),
                               7)

        # Drawing output layer texts
        FirstNeuronText = Font.render("Left", True, (0, 0, 0))
        SecondNeuronText = Font.render("Right", True, (0, 0, 0))
        ThirdNeuronText = Font.render("Up", True, (0, 0, 0))
        FourthNeuronText = Font.render("Down", True, (0, 0, 0))
        FifthNeuronText = Font.render("Craft", True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(FirstNeuronText, (initial_x_loc + 160, initial_y_loc - 13))
        self.CurrentBackground.Screen.blit(SecondNeuronText,
                                           (initial_x_loc + 160, initial_y_loc + 1 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(ThirdNeuronText,
                                           (initial_x_loc + 160, initial_y_loc + 2 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(FourthNeuronText,
                                           (initial_x_loc + 160, initial_y_loc + 3 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(FifthNeuronText,
                                           (initial_x_loc + 160, initial_y_loc + 4 * EachNeuronOffset - 13))

        # Drawing connections
        for i in range(len(BestCharacterBrain.EntryLayer.Neurons) - BIAS):
            for j in range(len(BestCharacterBrain.HiddenLayers[0].Neurons) - BIAS):
                if BestCharacterBrain.EntryLayer.Neurons[i].OutValue > 0 and BestCharacterBrain.HiddenLayers[0].Neurons[
                    j].OutValue > 0:
                    pygame.draw.line(self.CurrentBackground.Screen, NeuronActiveColor,
                                     (initial_x_loc + 50, initial_y_loc + i * EachNeuronOffset),
                                     (initial_x_loc + 100, initial_y_loc + j * EachNeuronOffset), 1)
                else:
                    pygame.draw.line(self.CurrentBackground.Screen, (0, 0, 0),
                                     (initial_x_loc + 50, initial_y_loc + i * EachNeuronOffset),
                                     (initial_x_loc + 100, initial_y_loc + j * EachNeuronOffset), 1)
        if len(BestCharacterBrain.HiddenLayers) > 1:
            for i in range(len(BestCharacterBrain.HiddenLayers[0].Neurons) - BIAS):
                for j in range(len(BestCharacterBrain.HiddenLayers[1].Neurons) - BIAS):
                    if BestCharacterBrain.HiddenLayers[0].Neurons[i].OutValue > 0:
                        pygame.draw.line(self.CurrentBackground.Screen, NeuronActiveColor,
                                         (initial_x_loc + 100, initial_y_loc + i * EachNeuronOffset),
                                         (initial_x_loc + 150, initial_y_loc + j * EachNeuronOffset), 1)
                    else:
                        pygame.draw.line(self.CurrentBackground.Screen, (0, 0, 0),
                                         (initial_x_loc + 100, initial_y_loc + i * EachNeuronOffset),
                                         (initial_x_loc + 150, initial_y_loc + j * EachNeuronOffset), 1)
        for i in range(len(BestCharacterBrain.HiddenLayers[-1].Neurons) - BIAS):
            for j in range(len(BestCharacterBrain.LastCalculatedOutput)):
                if BestCharacterBrain.HiddenLayers[-1].Neurons[i].OutValue > 0 and \
                        BestCharacterBrain.LastCalculatedOutput[j] != 0:
                    pygame.draw.line(self.CurrentBackground.Screen, NeuronActiveColor,
                                     (initial_x_loc + 100, initial_y_loc + i * EachNeuronOffset),
                                     (initial_x_loc + 150, initial_y_loc + j * EachNeuronOffset), 1)
                else:
                    pygame.draw.line(self.CurrentBackground.Screen, (0, 0, 0),
                                     (initial_x_loc + 100, initial_y_loc + i * EachNeuronOffset),
                                     (initial_x_loc + 150, initial_y_loc + j * EachNeuronOffset), 1)

    def DrawInfo(self):
        InitialYLoc = 0
        InitialXLoc = self.CurrentBackground.DisplayWidth
        pygame.draw.rect(self.CurrentBackground.Screen, (255, 255, 255), (InitialXLoc, InitialYLoc, 275, 300))

        self.DrawCurrentGeneration(InitialXLoc, InitialYLoc)
        self.GetBestFiveCharacters()
        self.DrawBestFitness(InitialXLoc, InitialYLoc + 15)
        self.DrawNeuralNet(InitialXLoc, InitialYLoc + 60)
