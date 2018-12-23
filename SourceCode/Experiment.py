from Visualization import DrawBackground,DrawNewState,DrawImage
from Controller import HumanController
import UpdateWorld
from Writer import WriteDataFrameToCSV
import pygame as pg
from pygame import time
import os
import pandas as pd
from Trial import Trial
import collections as co

class Experiment():
	def __init__(self,trial,initialWorld,updateWorld,drawImage,resultsPath,introductionImage,restImage,finishImage,minDistanceBetweenGrids):
		self.trial=trial
		self.initialWorld=initialWorld
		self.updateWorld=updateWorld
		self.drawImage=drawImage
		self.resultsPath=resultsPath
		self.introductionImage=introductionImage
		self.restImage=restImage
		self.finishImage=finishImage
		self.minDistanceBetweenGrids=minDistanceBetweenGrids

	def __call__(self,restTime,finishTime):
		restFlag=[False]*len(restTime)
		numberOfRests=0
		values=co.OrderedDict()
		values["name"] = input("Please enter your name:").capitalize()
		values["order"] = input("Please enter your order:").capitalize()
		values["testOrExperiment"] = input("test or experiment? ").capitalize()
		values["condition"]='None'
		writerPath=self.resultsPath+values["name"]+values["order"]+values["testOrExperiment"]+'.csv'
		writer=WriteDataFrameToCSV(writerPath)
		self.drawImage(self.introductionImage)
		bean1Grid, bean2Grid, playerGrid = self.initialWorld(self.minDistanceBetweenGrids)
		initialTime=time.get_ticks()
		trialIndex=0
		while True:
			results, bean1Grid, playerGrid, action=self.trial(bean1Grid, bean2Grid, playerGrid)
			response=values.copy()
			response.update(results)
			responseDF=pd.DataFrame(response,index=[trialIndex])
			writer(responseDF)
			bean2Grid,values["condition"]=self.updateWorld(bean1Grid, playerGrid, action)
			trialIndex+=1
			if time.get_ticks()-initialTime>=finishTime:
				self.drawImage(self.finishImage)
				break
			elif time.get_ticks()-initialTime>=restTime[numberOfRests] and restFlag[numberOfRests]==False:
				self.drawImage(self.restImage)
				restFlag[numberOfRests] = True
				numberOfRests=min(numberOfRests+1,len(restTime)-1)
		return 0



def main():
	dimension = 21
	bounds = [0, 0, dimension - 1, dimension - 1]
	minDistanceBetweenGrids = 5
	condition = [-5, -3, -1, 0, 1, 3, 5]
	counter = [0] * len(condition)
	initialWorld = UpdateWorld.InitialWorld(bounds)
	updateWorld = UpdateWorld.UpdateWorld(bounds, condition, counter, minDistanceBetweenGrids)
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
	stopwatchUnit=100
	finishTime=1000*60*20
	restTime=list(range(1000*60*5,1000*60*20,1000*60*5))
	stopwatchEvent = pg.USEREVENT + 1
	pg.time.set_timer(stopwatchEvent, stopwatchUnit)
	pg.event.set_allowed([pg.KEYDOWN, pg.QUIT, stopwatchEvent])
	picturePath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Pictures/'
	resultsPath= os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/'
	introductionImage = pg.image.load(picturePath + 'introduction.png')
	restImage = pg.image.load(picturePath + 'rest.png')
	finishImage = pg.image.load(picturePath + 'finish.png')
	drawBackground = DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth)
	drawNewState = DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
	drawImage = DrawImage(screen)
	humanController = HumanController(gridSize,stopwatchEvent,stopwatchUnit)
	trial = Trial(humanController, drawNewState,stopwatchEvent)
	experiment=Experiment(trial,initialWorld,updateWorld,drawImage,resultsPath,introductionImage,restImage,finishImage,minDistanceBetweenGrids)
	experiment(restTime,finishTime)


if __name__ == "__main__":
	main()
