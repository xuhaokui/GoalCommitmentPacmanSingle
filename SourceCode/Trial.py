import numpy as np
from Visualization import DrawBackground,DrawNewState,DrawImage
from Controller import HumanController
import UpdateWorld
import pygame as pg
import collections as co
from pygame import time


class Trial():
	def __init__(self,humanController,drawNewState):
		self.humanController=humanController
		self.drawNewState=drawNewState

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
		initialTime = time.get_ticks()
		results=co.OrderedDict()
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP])
		firstActionFlag=False
		self.drawNewState(bean1Grid, bean2Grid, playerGrid)
		while not firstActionFlag:
			playerGrid, action = self.humanController(playerGrid)
			self.drawNewState(bean1Grid, bean2Grid, playerGrid)
			eatenFlag = self.checkEaten(bean1Grid, bean2Grid, playerGrid)
			if action in self.humanController.actionDict.values():
				firstResponseTime=time.get_ticks()-initialTime
				firstActionFlag=True
		while pause:
			playerGrid,action=self.humanController(playerGrid)
			self.drawNewState(bean1Grid, bean2Grid, playerGrid)
			eatenFlag=self.checkEaten(bean1Grid, bean2Grid,playerGrid)
			pause=self.checkTerminationOfTrial(action,eatenFlag)
		pg.event.set_blocked([pg.KEYDOWN, pg.KEYUP])
		wholeResponseTime=time.get_ticks()-initialTime
		self.drawNewState(bean1Grid, bean2Grid, playerGrid)
		results["bean1GridX"] = bean1Grid[0]
		results["bean1GridY"] = bean1Grid[1]
		results["bean2GridX"] = bean2Grid[0]
		results["bean2GridY"] = bean2Grid[1]
		results["playerGridX"] = playerGrid[0]
		results["playerGridY"] = playerGrid[1]
		if (True in eatenFlag):results["beanEaten"] = eatenFlag.index(True)+1
		results["firstResponseTime"]=firstResponseTime
		results["trialTime"]=wholeResponseTime
		return results,action





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
	drawBackground = DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth)
	drawNewState = DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
	humanController=HumanController(gridSize)
	trial=Trial(humanController,drawNewState)
	bean1Grid,bean2Grid,playerGrid=initialWorld(minDistanceBetweenGrids)
	results=trial(bean1Grid,bean2Grid,playerGrid)
	print(results)

if __name__=="__main__":
	main()
