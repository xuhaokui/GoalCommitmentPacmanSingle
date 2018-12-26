import numpy as np
import pygame as pg
from pygame import time
import collections as co
import pickle
from Visualization import DrawBackground,DrawNewState,DrawImage
from Controller import HumanController,ModelController
import UpdateWorld


class Trial():
	def __init__(self,humanController,drawNewState,stopwatchEvent,finishTime):
		self.humanController=humanController
		self.drawNewState=drawNewState
		self.stopwatchEvent=stopwatchEvent
		self.finishTime=finishTime

	def checkEaten(self,bean1Grid, bean2Grid, humanGrid):
		if np.linalg.norm(np.array(humanGrid) - np.array(bean1Grid), ord=1)==0:
			eatenFlag=[True,False]
		elif np.linalg.norm(np.array(humanGrid) - np.array(bean2Grid), ord=1) == 0:
			eatenFlag=[False,True]
		else:
			eatenFlag=[False,False]
		return eatenFlag

	def checkTerminationOfTrial(self,action,eatenFlag,currentStopwatch):
		if np.any(eatenFlag)==True or action==pg.QUIT or currentStopwatch>=self.finishTime:
			pause=False
		else:
			pause=True
		return pause

	def __call__(self,bean1Grid,bean2Grid,playerGrid,score,currentStopwatch):
		pause=True
		initialPlayerGrid=playerGrid
		initialTime = time.get_ticks()
		results=co.OrderedDict()
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP,pg.QUIT,self.stopwatchEvent])
		playerGrid, action, currentStopwatch = self.humanController(bean1Grid, bean2Grid, playerGrid, score,currentStopwatch)
		eatenFlag = self.checkEaten(bean1Grid, bean2Grid, playerGrid)
		firstResponseTime = time.get_ticks() - initialTime
		while pause:
			playerGrid,action,currentStopwatch =self.humanController(bean1Grid, bean2Grid, playerGrid, score,currentStopwatch)
			eatenFlag=self.checkEaten(bean1Grid, bean2Grid,playerGrid)
			score=np.add(score,np.sum(eatenFlag))
			pause=self.checkTerminationOfTrial(action,eatenFlag,currentStopwatch)
		self.drawNewState(bean1Grid, bean2Grid, playerGrid, currentStopwatch,score)
		wholeResponseTime=time.get_ticks() - initialTime
		pg.event.set_blocked([pg.KEYDOWN, pg.KEYUP])
		results["bean1GridX"] = bean1Grid[0]
		results["bean1GridY"] = bean1Grid[1]
		results["bean2GridX"] = bean2Grid[0]
		results["bean2GridY"] = bean2Grid[1]
		results["playerGridX"] = initialPlayerGrid[0]
		results["playerGridY"] = initialPlayerGrid[1]
		if True in eatenFlag:
			results["beanEaten"] = eatenFlag.index(True)+1
			oldGrid=eval('bean'+str(eatenFlag.index(False)+1)+'Grid')
		else:
			results["beanEaten"] = 0
			oldGrid=None
		results["firstResponseTime"]=firstResponseTime
		results["trialTime"]=wholeResponseTime
		return results,oldGrid,playerGrid,score,currentStopwatch





def main():
	dimension = 21
	bounds = [0, 0, dimension - 1, dimension - 1]
	minDistanceBetweenGrids = 5
	condition = [-5, -3, -1, 0, 1, 3, 5]
	initialWorld = UpdateWorld.InitialWorld(bounds)
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
	stopwatchUnit=10
	textColorTuple=(255,50,50)
	stopwatchEvent = pg.USEREVENT + 1
	pg.time.set_timer(stopwatchEvent, stopwatchUnit)
	pg.event.set_allowed([pg.KEYDOWN, pg.QUIT, stopwatchEvent])
	finishTime=90000
	currentStopwatch=32888
	score=0
	drawBackground = DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth, textColorTuple)
	drawNewState = DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
	humanController=HumanController(gridSize, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)
	policy=pickle.load(open("SingleWolfTwoSheepsGrid15.pkl","rb"))
	modelController=ModelController(policy, gridSize, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)
	trial=Trial(modelController, drawNewState, stopwatchEvent, finishTime)
	bean1Grid,bean2Grid,playerGrid=initialWorld(minDistanceBetweenGrids)
	bean1Grid=(3,13)
	bean2Grid=(5,0)
	playerGrid=(0,8)
	results=trial(bean1Grid, bean2Grid, playerGrid, score, currentStopwatch)


if __name__=="__main__":
	main()

