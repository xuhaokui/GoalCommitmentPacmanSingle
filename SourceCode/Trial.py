import numpy as np
import pygame as pg
from pygame import time
import collections as co
from Visualization import DrawBackground,DrawNewState,DrawImage
from Controller import HumanController
import UpdateWorld


class Trial():
	def __init__(self,humanController,drawNewState,stopwatchEvent):
		self.humanController=humanController
		self.drawNewState=drawNewState
		self.stopwatchEvent=stopwatchEvent
		self.score=0

	def checkEaten(self,bean1Grid, bean2Grid, humanGrid):
		if np.linalg.norm(np.array(humanGrid) - np.array(bean1Grid), ord=1)==0:
			eatenFlag=[True,False]
		elif np.linalg.norm(np.array(humanGrid) - np.array(bean2Grid), ord=1) == 0:
			eatenFlag=[False,True]
		else:
			eatenFlag=[False,False]
		return eatenFlag

	def checkTerminationOfTrial(self,action,eatenFlag):
		if np.any(eatenFlag)==True or action==pg.QUIT :
			pause=False
		else:
			pause=True
		return pause

	def __call__(self,bean1Grid,bean2Grid,playerGrid):
		pause=True
		score=self.score
		initialPlayerGrid=playerGrid
		initialTime = time.get_ticks()
		results=co.OrderedDict()
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP,pg.QUIT,self.stopwatchEvent])
		self.drawNewState(bean1Grid, bean2Grid, playerGrid)
		playerGrid, action,stopwatch = self.humanController(playerGrid)
		eatenFlag = self.checkEaten(bean1Grid, bean2Grid, playerGrid)
		firstResponseTime = time.get_ticks() - initialTime
		while pause:
			self.drawNewState(bean1Grid, bean2Grid, playerGrid)
			playerGrid,action,stopwatch=self.humanController(playerGrid,score)
			eatenFlag=self.checkEaten(bean1Grid, bean2Grid,playerGrid)
			pause=self.checkTerminationOfTrial(action,eatenFlag)

		wholeResponseTime=time.get_ticks() - initialTime
		pg.event.set_blocked([pg.KEYDOWN, pg.KEYUP])
		self.drawNewState(bean1Grid, bean2Grid, playerGrid)
		results["bean1GridX"] = bean1Grid[0]
		results["bean1GridY"] = bean1Grid[1]
		results["bean2GridX"] = bean2Grid[0]
		results["bean2GridY"] = bean2Grid[1]
		results["playerGridX"] = initialPlayerGrid[0]
		results["playerGridY"] = initialPlayerGrid[1]
		if True in eatenFlag:
			results["beanEaten"] = eatenFlag.index(True)+1
			oldGrid=eval('bean'+str(eatenFlag.index(False)+1)+'Grid')
			self.score+=1
		else:
			results["beanEaten"] = 0
			oldGrid=None
		results["firstResponseTime"]=firstResponseTime
		results["trialTime"]=wholeResponseTime
		return results,oldGrid,playerGrid,action





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
	stopwatchUnit=100
	stopwatchEvent = pg.USEREVENT + 1
	pg.time.set_timer(stopwatchEvent, stopwatchUnit)
	pg.event.set_allowed([pg.KEYDOWN, pg.QUIT, stopwatchEvent])
	drawBackground = DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth)
	drawNewState = DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
	humanController=HumanController(gridSize,stopwatchEvent,stopwatchUnit)
	trial=Trial(humanController,drawNewState,stopwatchEvent)
	bean1Grid,bean2Grid,playerGrid=initialWorld(minDistanceBetweenGrids)
	results=trial(bean1Grid,bean2Grid,playerGrid)


if __name__=="__main__":
	main()
