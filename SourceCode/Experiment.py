import pygame as pg
import os
import pandas as pd
import collections as co
import numpy as np
from Visualization import DrawBackground, DrawNewState, DrawImage
from Controller import HumanController
import UpdateWorld
from Writer import WriteDataFrameToCSV
from Trial import Trial


class Experiment():
    def __init__(self, trial, writer, experimentValues, initialWorld, updateWorld, drawImage, resultsPath, \
                 minDistanceBetweenGrids):
        self.trial = trial
        self.writer = writer
        self.experimentValues = experimentValues
        self.initialWorld = initialWorld
        self.updateWorld = updateWorld
        self.drawImage = drawImage
        self.resultsPath = resultsPath
        self.minDistanceBetweenGrids = minDistanceBetweenGrids

    def __call__(self, finishTime,image):
        bean1Grid, bean2Grid, playerGrid = self.initialWorld(self.minDistanceBetweenGrids)
        trialIndex = 0
        score=0
        currentStopwatch=0
        while True:
            results, bean1Grid, playerGrid,score,currentStopwatch = self.trial(bean1Grid, bean2Grid, playerGrid,score,currentStopwatch)
            response = self.experimentValues.copy()
            response.update(results)
            responseDF = pd.DataFrame(response, index=[trialIndex])
            self.writer(responseDF)
            if currentStopwatch >= finishTime:
                self.drawImage(image)
                break
            bean2Grid, self.experimentValues["condition"] = self.updateWorld(bean1Grid, playerGrid)
            trialIndex += 1
        return score


def main():
    gridSize = 15
    bounds = [0, 0, gridSize - 1, gridSize - 1]
    minDistanceBetweenGrids = 5
    condition = [-5, -3, -1, 0, 1, 3, 5]
    counter = [0] * len(condition)
    initialWorld = UpdateWorld.InitialWorld(bounds)
    updateWorld = UpdateWorld.UpdateWorld(bounds, condition, counter)
    pg.init()
    screenWidth = 720
    screenHeight = 720
    screen = pg.display.set_mode((screenWidth, screenHeight))
    leaveEdgeSpace = 2
    lineWidth = 1
    backgroundColor = [205, 255, 204]
    lineColor = [0, 0, 0]
    targetColor = [255, 50, 50]
    playerColor = [50, 50, 255]
    targetRadius = 10
    playerRadius = 10
    stopwatchUnit = 1000
    finishTime=1000*90
    numberOfRests=4
    textColorTuple = (255, 50, 50)
    stopwatchEvent = pg.USEREVENT + 1
    pg.time.set_timer(stopwatchEvent, stopwatchUnit)
    pg.event.set_allowed([pg.KEYDOWN, pg.QUIT, stopwatchEvent])
    picturePath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Pictures/'
    resultsPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/'
    experimentValues = co.OrderedDict()
    experimentValues["name"] = input("Please enter your name:").capitalize()
    experimentValues["condition"] = 'None'
    writerPath = resultsPath + experimentValues["name"] + '.csv'
    writer = WriteDataFrameToCSV(writerPath)
    introductionImage = pg.image.load(picturePath + 'introduction.png')
    restImage = pg.image.load(picturePath + 'rest.png')
    finishImage = pg.image.load(picturePath + 'finish.png')
    introductionImage=pg.transform.scale(introductionImage, (screenWidth,screenHeight))
    finishImage=pg.transform.scale(finishImage, (int(screenWidth*2/3),int(screenHeight/4)))
    drawBackground = DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth,
                                    textColorTuple)
    drawNewState = DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
    drawImage = DrawImage(screen)
    humanController = HumanController(gridSize, stopwatchEvent, stopwatchUnit, drawNewState)
    trial = Trial(humanController, drawNewState, stopwatchEvent,finishTime)
    experiment = Experiment(trial, writer, experimentValues, initialWorld, updateWorld, drawImage, resultsPath,
                             minDistanceBetweenGrids)
    drawImage(introductionImage)
    score=[0]*numberOfRests
    for i in range(numberOfRests):
        if i == numberOfRests-1:
            score[i]=experiment(finishTime,finishImage)
        else:
            score[i]=experiment(finishTime,restImage)
    participantsScore=np.sum(np.array(score))
    print(participantsScore)

if __name__ == "__main__":
    main()
