
import numpy as np 
import pygame as pg 

class HumanController():
	def __init__(self,gridSize):
		self.actionDict={pg.K_UP:[0,-1], pg.K_DOWN:[0,1], pg.K_LEFT:[-1,0], pg.K_RIGHT:[1,0]}
		self.gridSize=gridSize
	def __call__(self,playerPosition):
		pause=True
		while pause:
			pg.time.wait(10)
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key in self.actionDict.keys():
					pause=False
					action = self.actionDict[event.key]
		playerNextPosition = np.add(playerPosition,action)
		if np.any(playerNextPosition<0) or np.any(playerNextPosition>self.gridSize):
			playerNextPosition = playerPosition.copy()
		return playerNextPosition

class ModelController():
	def __init__(self):
		pass
	def __call__(self):
		return

if __name__=="__main__":
	pg.init()
	playerPosition=[10,20]
	gridSize=20

	getHumanAction = HumanController(gridSize)

	playerNextPosition=getHumanAction(playerPosition)
	print(playerNextPosition)
