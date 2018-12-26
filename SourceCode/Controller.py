import numpy as np
import pygame as pg
import random
import Visualization

class HumanController():
	def __init__(self,gridSize,stopwatchEvent,stopwatchUnit,drawNewState,finishTime):
		self.actionDict={pg.K_UP:[0,-1], pg.K_DOWN:[0,1], pg.K_LEFT:[-1,0], pg.K_RIGHT:[1,0]}
		self.gridSize=gridSize
		self.stopwatchEvent=stopwatchEvent
		self.stopwatchUnit=stopwatchUnit
		self.stopwatch=0
		self.drawNewState=drawNewState
		self.finishTime=finishTime

	def __call__(self,targetPositionA,targetPositionB,playerPosition,currentScore,currentStopwatch):
		pause=True
		playerNextPosition=playerPosition.copy()
		newStopwatch = currentStopwatch
		remainningTime=max(0,self.finishTime-currentStopwatch)
		self.drawNewState(targetPositionA,targetPositionB,playerPosition,remainningTime,currentScore)
		while pause:
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key in self.actionDict.keys() and \
						np.all(np.add(playerPosition,self.actionDict[event.key])>=0) and \
						np.all(np.add(playerPosition,self.actionDict[event.key])<self.gridSize)\
						and event.type!=self.stopwatchEvent:
					action = self.actionDict[event.key]
					playerNextPosition = np.add(playerPosition,action)
					# newStopwatch = currentStopwatch
					pause=False
				elif event.type == pg.QUIT:
					action=pg.QUIT
					playerNextPosition = playerPosition.copy()
					# newStopwatch = currentStopwatch
					pause=False
				elif event.type == self.stopwatchEvent:
					action='None'
					newStopwatch=newStopwatch+self.stopwatchUnit
					playerNextPosition =playerPosition
					# pause=False
				# elif event.type == pg.KEYDOWN and event.key in self.actionDict.keys() and event.type == self.stopwatchEvent:
				# 	action = self.actionDict[event.key]
				# 	playerNextPosition = np.add(playerPosition, action)
				# 	newStopwatch = currentStopwatch + self.stopwatchUnit
				# 	pause=False
				# else:
				# 	action='None'
				# 	playerNextPosition=playerPosition
				# 	newStopwatch=currentStopwatch
				# 	pause=False
			remainningTime=max(0,self.finishTime - newStopwatch)
			self.drawNewState(targetPositionA,targetPositionB,playerNextPosition,remainningTime,currentScore)
			pg.display.flip()
		return playerNextPosition,action,newStopwatch

class ModelController():
	def __init__(self,policy,gridSize,stopwatchEvent,stopwatchUnit,drawNewState,finishTime):
		self.policy=policy
		self.gridSize=gridSize
		self.stopwatchEvent=stopwatchEvent
		self.stopwatchUnit=stopwatchUnit
		self.stopwatch=0
		self.drawNewState=drawNewState
		self.finishTime=finishTime
	def __call__(self,targetPositionA,targetPositionB,playerPosition,currentScore,currentStopwatch):
		pause=True
		newStopwatch = currentStopwatch
		remainningTime=max(0,self.finishTime-currentStopwatch)
		self.drawNewState(targetPositionA,targetPositionB,playerPosition,remainningTime,currentScore)
		while pause:
			targetStates = (tuple(targetPositionA),tuple(targetPositionB))
			if targetStates not in self.policy.keys():
				targetStates = (tuple(targetPositionB),tuple(targetPositionA))
			policyForCurrentStateDict=self.policy[targetStates][tuple(playerPosition)]
			actionMaxList = [action for action in policyForCurrentStateDict.keys() if policyForCurrentStateDict[action]==np.max(list(policyForCurrentStateDict.values()))]
			action = random.choice(actionMaxList)
			playerNextPosition=np.add(playerPosition,action)
			if np.any(playerNextPosition<0) or np.any(playerNextPosition>=self.gridSize):
				playerNextPosition=playerPosition
			pause=False
			for event in pg.event.get():
				if event.type == self.stopwatchEvent:
					newStopwatch=newStopwatch+self.stopwatchUnit
					remainningTime=max(0,self.finishTime - newStopwatch)
			self.drawNewState(targetPositionA,targetPositionB,playerNextPosition,remainningTime,currentScore)
			pg.display.flip()
		return playerNextPosition,action,newStopwatch

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
	finishTime=90000
	currentStopwatch=32000

	drawBackground=Visualization.DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth, textColorTuple)
	drawNewState=Visualization.DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)

	getHumanAction = HumanController(gridSize, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)
	import pickle
	policy=pickle.load(open("SingleWolfTwoSheepsGrid15.pkl","rb"))
	getModelAction = ModelController(policy, gridSize, stopwatchEvent, stopwatchUnit, drawNewState, finishTime)

	# [playerNextPosition,action,newStopwatch]=getHumanAction(targetPositionA, targetPositionB, playerPosition, currentScore, currentStopwatch)
	[playerNextPosition,action,newStopwatch]=getModelAction(targetPositionA, targetPositionB, playerPosition, currentScore, currentStopwatch)
	print(playerNextPosition,action,newStopwatch)

	pg.quit()
