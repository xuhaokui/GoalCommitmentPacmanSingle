import pygame as pg
from pygame import time
import os
import pandas as pd
import collections as co
from Visualization import DrawBackground, DrawNewState, DrawImage
from Controller import HumanController
import UpdateWorld
from Writer import WriteDataFrameToCSV
from Trial import Trial


class Experiment():
    def __init__(self, trial, writer, experimentValues, initialWorld, updateWorld, drawImage, resultsPath, \
                 introductionImage,  minDistanceBetweenGrids):
        self.trial = trial
        self.writer = writer
        self.experimentValues = experimentValues
        self.initialWorld = initialWorld
        self.updateWorld = updateWorld
        self.drawImage = drawImage
        self.resultsPath = resultsPath
        self.introductionImage = introductionImage
        self.minDistanceBetweenGrids = minDistanceBetweenGrids

    def __call__(self, finishTime,image):
        self.drawImage(self.introductionImage)
        bean1Grid, bean2Grid, playerGrid = self.initialWorld(self.minDistanceBetweenGrids)
        initialTime = time.get_ticks()
        trialIndex = 0
        score=0
        while True:
            results, bean1Grid, playerGrid,score = self.trial(bean1Grid, bean2Grid, playerGrid,score)
            response = self.experimentValues.copy()
            response.update(results)
            responseDF = pd.DataFrame(response, index=[trialIndex])
            self.writer(responseDF)
            bean2Grid, self.experimentValues["condition"] = self.updateWorld(bean1Grid, playerGrid)
            trialIndex += 1
            if time.get_ticks() - initialTime >= finishTime:
                self.drawImage(image)
                break


def main():
    dimension = 21
    bounds = [0, 0, dimension - 1, dimension - 1]
    minDistanceBetweenGrids = 5
    condition = [-5, -3, -1, 0, 1, 3, 5]
    counter = [0] * len(condition)
    initialWorld = UpdateWorld.InitialWorld(bounds)
    updateWorld = UpdateWorld.UpdateWorld(bounds, condition, counter)
    pg.init()
    screenWidth = 720
    screenHeight = 720
    screen = pg.display.set_mode((screenWidth, screenHeight))
    gridSize = 21
    leaveEdgeSpace = 2
    lineWidth = 1
    backgroundColor = [205, 255, 204]
    lineColor = [0, 0, 0]
    targetColor = [255, 50, 50]
    playerColor = [50, 50, 255]
    targetRadius = 10
    playerRadius = 10
    stopwatchUnit = 100
    finishTime = 1000 * 60 * 5
    numberOfRests=4
    textColorTuple = (255, 50, 50)
    stopwatchEvent = pg.USEREVENT + 1
    pg.time.set_timer(stopwatchEvent, stopwatchUnit)
    pg.event.set_allowed([pg.KEYDOWN, pg.QUIT, stopwatchEvent])
    picturePath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Pictures/'
    resultsPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/'
    experimentValues = co.OrderedDict()
    experimentValues["name"] = input("Please enter your name:").capitalize()
    experimentValues["order"] = input("Please enter your order:").capitalize()
    experimentValues["testOrExperiment"] = input("test or experiment? ").capitalize()
    experimentValues["condition"] = 'None'
    writerPath = resultsPath + experimentValues["name"] + experimentValues["order"] + experimentValues[
        "testOrExperiment"] + '.csv'
    writer = WriteDataFrameToCSV(writerPath)
    introductionImage = pg.image.load(picturePath + 'rest.png')
    restImage = pg.image.load(picturePath + 'rest.png')
    finishImage = pg.image.load(picturePath + 'rest.png')
    drawBackground = DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth,
                                    textColorTuple)
    drawNewState = DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
    drawImage = DrawImage(screen)
    humanController = HumanController(gridSize, stopwatchEvent, stopwatchUnit, drawNewState)
    trial = Trial(humanController, drawNewState, stopwatchEvent)
    experiment = Experiment(trial, writer, experimentValues, initialWorld, updateWorld, drawImage, resultsPath,
                            introductionImage, minDistanceBetweenGrids)
    for i in range(numberOfRests):
        if i == numberOfRests-1:
            experiment(finishTime,finishImage)
        else:
            experiment(finishTime,restImage)


if __name__ == "__main__":
    main()
