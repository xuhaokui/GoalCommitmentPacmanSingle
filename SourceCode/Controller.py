import numpy as np
import pygame as pg
import Visualization

class HumanController():
	def __init__(self,gridSize,stopwatchEvent,stopwatchUnit,drawNewState):
		self.actionDict={pg.K_UP:[0,-1], pg.K_DOWN:[0,1], pg.K_LEFT:[-1,0], pg.K_RIGHT:[1,0]}
		self.gridSize=gridSize
		self.stopwatchEvent=stopwatchEvent
		self.stopwatchUnit=stopwatchUnit
		self.stopwatch=0
		self.drawNewState=drawNewState
	def __call__(self,targetPositionA,targetPositionB,playerPosition,currentScore):
		pause=True
		playerNextPosition=playerPosition.copy()
		while pause:
			# pg.time.wait(10)
			self.drawNewState(targetPositionA,targetPositionB,playerNextPosition,self.stopwatch,currentScore)
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key in self.actionDict.keys() and np.all(np.add(playerPosition,self.actionDict[event.key])>=0) and np.all(np.add(playerPosition,self.actionDict[event.key])<self.gridSize):
					pause=False
					action = self.actionDict[event.key]
					playerNextPosition = np.add(playerPosition,action)
					self.drawNewState(targetPositionA,targetPositionB,playerNextPosition,self.stopwatch,currentScore)
				elif event.type == pg.QUIT:
					pause=False
					action=pg.QUIT
					playerNextPosition = playerPosition.copy()
				if event.type == self.stopwatchEvent:
					self.stopwatch=self.stopwatch+self.stopwatchUnit
		# if np.any(playerNextPosition<0) or np.any(playerNextPosition>=self.gridSize):
		# 	playerNextPosition = playerPosition.copy()
		return playerNextPosition,action,self.stopwatch

class ModelController():
	def __init__(self):
		pass
	def __call__(self):
		return

if __name__=="__main__":
	pg.init()
	screenWidth=720
	screenHeight=720
	screen=pg.display.set_mode((screenWidth,screenHeight))
	gridSize=20
	leaveEdgeSpace=2
	lineWidth=2
	backgroundColor=[188,188,0]
	lineColor=[255,255,255]
	targetColor=[255,50,50]
	playerColor=[50,50,255]
	targetRadius=10
	playerRadius=10
	targetPositionA=[5,5]
	targetPositionB=[15,5]
	playerPosition=[10,15]
	currentScore=5
	textColorTuple=(255,50,50)
	stopwatchEvent = pg.USEREVENT + 1
	stopwatchUnit=10
	pg.time.set_timer(stopwatchEvent, stopwatchUnit)

	drawBackground=Visualization.DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth, textColorTuple)
	drawNewState=Visualization.DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)

	getHumanAction = HumanController(gridSize, stopwatchEvent, stopwatchUnit, drawNewState)

	[playerNextPosition,action,stopwatch]=getHumanAction(targetPositionA, targetPositionB, playerPosition, currentScore)
	print(playerNextPosition,action,stopwatch)
