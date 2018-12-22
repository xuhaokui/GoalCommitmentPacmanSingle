
import pygame as pg 
import numpy as np 
import os 
import time

class DrawBackground():
	def __init__(self,screen,gridSize,leaveEdgeSpace,backgroundColor,lineColor,lineWidth):
		self.screen=screen
		self.gridSize=gridSize
		self.leaveEdgeSpace=leaveEdgeSpace
		self.widthLineStepSpace=np.int(screen.get_width()/(gridSize+2*self.leaveEdgeSpace))
		self.heightLineStepSpace=np.int(screen.get_height()/(gridSize+2*self.leaveEdgeSpace))
		self.backgroundColor=backgroundColor
		self.lineColor=lineColor
		self.lineWidth=lineWidth
	def __call__(self):
		for drawtime in range(1):
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					break
			self.screen.fill((0,0,0))
			pg.draw.rect(self.screen,self.backgroundColor,pg.Rect(np.int(self.leaveEdgeSpace*self.widthLineStepSpace),np.int(self.leaveEdgeSpace*self.heightLineStepSpace),
				np.int(self.gridSize*self.widthLineStepSpace),np.int(self.gridSize*self.heightLineStepSpace)))
			# time0=time.time()
			for i in range(self.gridSize+1):
				pg.draw.line(self.screen, self.lineColor, [np.int((i+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int(self.leaveEdgeSpace*self.heightLineStepSpace)], 
					[np.int((i+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int((self.gridSize+self.leaveEdgeSpace)*self.heightLineStepSpace)], self.lineWidth)
				pg.draw.line(self.screen, self.lineColor, [np.int(self.leaveEdgeSpace*self.widthLineStepSpace),np.int((i+self.leaveEdgeSpace)*self.heightLineStepSpace)], 
					[np.int((self.gridSize+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int((i+self.leaveEdgeSpace)*self.heightLineStepSpace)], self.lineWidth)
			# pg.display.flip()
			# print('draw background',time.time()-time0)
			pg.time.wait(1)
		return

class DrawNewState():
	def __init__(self,screen,drawBackground,targetColor,playerColor,targetRadius,playerRadius):
		self.screen=screen
		self.drawBackground=drawBackground
		self.targetColor=targetColor
		self.playerColor=playerColor
		self.targetRadius=targetRadius
		self.playerRadius=playerRadius
		self.leaveEdgeSpace=drawBackground.leaveEdgeSpace
		self.widthLineStepSpace=drawBackground.widthLineStepSpace
		self.heightLineStepSpace=drawBackground.heightLineStepSpace
	def __call__(self,targetPositionA,targetPositionB,playerPosition):
		for drawtime in range(1):
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					break
			self.screen.fill((0,0,0))
			self.drawBackground()
			# time0=time.time()
			pg.draw.circle(self.screen, self.targetColor, [np.int((targetPositionA[0]+self.leaveEdgeSpace+0.5)*self.widthLineStepSpace),
				np.int((targetPositionA[1]+self.leaveEdgeSpace+0.5)*self.heightLineStepSpace)], self.targetRadius)
			pg.draw.circle(self.screen, self.targetColor, [np.int((targetPositionB[0]+self.leaveEdgeSpace+0.5)*self.widthLineStepSpace),
				np.int((targetPositionB[1]+self.leaveEdgeSpace+0.5)*self.heightLineStepSpace)], self.targetRadius)
			pg.draw.circle(self.screen, self.playerColor, [np.int((playerPosition[0]+self.leaveEdgeSpace+0.5)*self.widthLineStepSpace),
				np.int((playerPosition[1]+self.leaveEdgeSpace+0.5)*self.heightLineStepSpace)],self.playerRadius)
			pg.display.flip()
			# print('draw circles',time.time()-time0)
			pg.time.wait(1)
		return

class DrawImage():
	def __init__(self,screen):
		self.screen=screen
	def __call__(self,image):
		pause=True
		for drawtime in range(2):
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					break
			self.screen.fill((0,0,0))
			self.screen.blit(image,(0,self.screen.get_height()/4))
			pg.display.flip()
			while pause and drawtime==1:
				pg.time.wait(10)
				for event in pg.event.get():
					if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
						pause=False
			pg.time.wait(10)

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
	picturePath=os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/Pictures/'
	restImage=pg.image.load(picturePath+'rest.png')


	drawBackground=DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth)
	drawNewState=DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
	drawImage=DrawImage(screen)

	drawImage(restImage)
	pg.quit()






