import numpy as np
from Visualization import DrawBackground,DrawNewState,DrawImage
from Controller import HumanController
import UpdateWorld
import pygame as pg
import os
import time
import collections as co


class Trial():
	def __init__(self,updateWorld,humanController,drawNewState):
		self.updateWorld=updateWorld
		self.humanController=humanController
		self.drawNewState=drawNewState
		self.counter=0

	def checkEaten(self,bean1Grid, bean2Grid, humanGrid):
		if np.linalg.norm(humanGrid - bean1Grid, ord=1)==0:
			eatenFlag=[True,False]
		elif np.linalg.norm(humanGrid - bean2Grid, ord=1) == 0:
			eatenFlag=[False,True]
		else:
			eatenFlag=[False,False]
		return eatenFlag

	def checkTerminationOfTrial(self,event,eatenFlag):
		if np.any(eatenFlag)==True :
			pause=False
		else:
			pause=True
		return pause

	def updateTrajectory(self, action, trajectoryList, playerPosition):
		if action in self.humanController.actionDict.values():
			trajectoryList.append(playerPosition)
		return trajectoryList

	def updateResponseTime(self, action, responseTime):
		if action in self.humanController.actionDict.values():
			now = time.time()
			responseTime.append(now)
		return responseTime

	def __call__(self,bean1Grid,bean2Grid,playerGrid):
		pause=True
		self.counter=self.counter+1
		initialTime = time.time()
		responseTimeList=[initialTime]
		trajectoryList=[]
		results=co.OrderedDict()
		eatenFlag=[False,False]
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP])
		while pause:
			self.drawNewState(bean1Grid, bean2Grid, playerGrid)
			playerGrid,action=self.humanController(playerGrid)
			trajectoryList = self.updateTrajectory(action, trajectoryList, playerGrid)
			responseTimeList = self.updateResponseTime(action, responseTimeList)
			eatenFlag=self.checkEaten(bean1Grid, bean2Grid,playerGrid)
			pause=self.checkTerminationOfTrial(action,eatenFlag)

		self.drawNewState(bean1Grid, bean2Grid, playerGrid)
		results["bean1GridX"] = bean1Grid[0]
		results["bean1GridY"] = bean1Grid[1]
		results["bean2GridX"] = bean2Grid[0]
		results["bean2GridY"] = bean2Grid[1]
		results["playerGridX"] = playerGrid[0]
		results["playerGridY"] = playerGrid[0]
		if (True in eatenFlag):results["beanEaten"] = eatenFlag.index(True)
		results["responseTime"]=str(responseTimeList)
		results["trajectory"]=str(trajectoryList)
		return results,action





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
	drawBackground = DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth)
	drawNewState = DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
	humanController=HumanController(gridSize)
	trial=Trial(updateWorld,humanController,drawNewState)
	bean1Grid,bean2Grid,playerGrid=initialWorld(minDistanceBetweenGrids)
	results=trial(bean1Grid,bean2Grid,playerGrid)
	print(results)

if __name__=="__main__":
	main()
