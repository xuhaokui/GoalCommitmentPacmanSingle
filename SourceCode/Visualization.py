<<<<<<< HEAD
import pygame as pg
import numpy as np
import os

def drawText(screen,text,textColorTuple,textPositionTuple):
	font = pg.font.Font(None,50)
	textObj=font.render(text, 1, textColorTuple)
	screen.blit(textObj,textPositionTuple)
	return

class GiveExperimentFeedback():
	def __init__(self,screen,textColorTuple,screenWidth,screenHeight):
		self.screen=screen
		self.textColorTuple=textColorTuple
		self.screenHeight=screenHeight
		self.screenWidth=screenWidth

	def __call__(self,trialIndex,score):
		self.screen.fill((0, 0, 0))
		for j in range(trialIndex + 1):
			drawText(self.screen,"No. "+ str(j+1)+ " experiment"  + "  score: " + str(score[j]), self.textColorTuple,
					 (self.screenWidth / 5, self.screenHeight * (j + 3) / 12))
		pg.display.flip()
		pg.time.wait(3000)

class DrawBackground():
	def __init__(self,screen,gridSize,leaveEdgeSpace,backgroundColor,lineColor,lineWidth,textColorTuple):
		self.screen=screen
		self.gridSize=gridSize
		self.leaveEdgeSpace=leaveEdgeSpace
		self.widthLineStepSpace=np.int(screen.get_width()/(gridSize+2*self.leaveEdgeSpace))
		self.heightLineStepSpace=np.int(screen.get_height()/(gridSize+2*self.leaveEdgeSpace))
		self.backgroundColor=backgroundColor
		self.lineColor=lineColor
		self.lineWidth=lineWidth
		self.textColorTuple=textColorTuple
	def __call__(self,currentTime,currentScore):
		self.screen.fill((0,0,0))
		pg.draw.rect(self.screen,self.backgroundColor,pg.Rect(np.int(self.leaveEdgeSpace*self.widthLineStepSpace),np.int(self.leaveEdgeSpace*self.heightLineStepSpace),
			np.int(self.gridSize*self.widthLineStepSpace),np.int(self.gridSize*self.heightLineStepSpace)))
		for i in range(self.gridSize+1):
			pg.draw.line(self.screen, self.lineColor, [np.int((i+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int(self.leaveEdgeSpace*self.heightLineStepSpace)],
				[np.int((i+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int((self.gridSize+self.leaveEdgeSpace)*self.heightLineStepSpace)], self.lineWidth)
			pg.draw.line(self.screen, self.lineColor, [np.int(self.leaveEdgeSpace*self.widthLineStepSpace),np.int((i+self.leaveEdgeSpace)*self.heightLineStepSpace)],
				[np.int((self.gridSize+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int((i+self.leaveEdgeSpace)*self.heightLineStepSpace)], self.lineWidth)
		seconds=currentTime/1000
		drawText(self.screen, 'Time: '+str("%4.1f" %seconds)+'s', self.textColorTuple, (self.widthLineStepSpace*2,self.leaveEdgeSpace*10))
		drawText(self.screen, 'Score: '+str(currentScore), self.textColorTuple, (self.widthLineStepSpace*13,self.leaveEdgeSpace*10))
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
	def __call__(self,targetPositionA,targetPositionB,playerPosition,currentTime,currentScore):
		self.drawBackground(currentTime,currentScore)
		pg.draw.circle(self.screen, self.targetColor, [np.int((targetPositionA[0]+self.leaveEdgeSpace+0.5)*self.widthLineStepSpace),
			np.int((targetPositionA[1]+self.leaveEdgeSpace+0.5)*self.heightLineStepSpace)], self.targetRadius)
		pg.draw.circle(self.screen, self.targetColor, [np.int((targetPositionB[0]+self.leaveEdgeSpace+0.5)*self.widthLineStepSpace),
			np.int((targetPositionB[1]+self.leaveEdgeSpace+0.5)*self.heightLineStepSpace)], self.targetRadius)
		pg.draw.circle(self.screen, self.playerColor, [np.int((playerPosition[0]+self.leaveEdgeSpace+0.5)*self.widthLineStepSpace),
			np.int((playerPosition[1]+self.leaveEdgeSpace+0.5)*self.heightLineStepSpace)],self.playerRadius)
		# pg.display.flip()
		return

class DrawImage():
	def __init__(self,screen):
		self.screen=screen
		self.screenCenter=(self.screen.get_width()/2,self.screen.get_height()/2)

	def __call__(self,image):
		imageRect=image.get_rect()
		imageRect.center=self.screenCenter
		pause=True
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP,pg.QUIT])
		self.screen.fill((0, 0, 0))
		self.screen.blit(image, imageRect)
		pg.display.flip()
		while pause:
			pg.time.wait(10)
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
					pause = False
				elif event.type == pg.QUIT:
					pg.quit()
			pg.time.wait(10)
		pg.event.set_blocked([pg.KEYDOWN, pg.KEYUP,pg.QUIT])


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
	currentTime=138456
	currentScore=5
	textColorTuple=(255,50,50)
	drawBackground=DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth, textColorTuple)
	drawNewState=DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
	drawImage=DrawImage(screen)
	drawBackground(currentTime, currentScore)
	pg.time.wait(5000)
	pg.quit()

=======
import pygame as pg
import numpy as np
import os

def drawText(screen,text,textColorTuple,textPositionTuple):
	font = pg.font.Font(None,50)
	textObj=font.render(text, 1, textColorTuple)
	screen.blit(textObj,textPositionTuple)
	return

class GiveExperimentFeedback():
	def __init__(self,screen,textColorTuple,screenWidth,screenHeight):
		self.screen=screen
		self.textColorTuple=textColorTuple
		self.screenHeight=screenHeight
		self.screenWidth=screenWidth

	def __call__(self,trialIndex,score):
		self.screen.fill((0, 0, 0))
		for j in range(trialIndex + 1):
			drawText(self.screen,"No. "+ str(j+1)+ " experiment"  + "  score: " + str(score[j]), self.textColorTuple,
					 (self.screenWidth / 5, self.screenHeight * (j + 3) / 12))
		pg.display.flip()
		pg.time.wait(3000)

class DrawBackground():
	def __init__(self,screen,gridSize,leaveEdgeSpace,backgroundColor,lineColor,lineWidth,textColorTuple):
		self.screen=screen
		self.gridSize=gridSize
		self.leaveEdgeSpace=leaveEdgeSpace
		self.widthLineStepSpace=np.int(screen.get_width()/(gridSize+2*self.leaveEdgeSpace))
		self.heightLineStepSpace=np.int(screen.get_height()/(gridSize+2*self.leaveEdgeSpace))
		self.backgroundColor=backgroundColor
		self.lineColor=lineColor
		self.lineWidth=lineWidth
		self.textColorTuple=textColorTuple
	def __call__(self,currentTime,currentScore):
		self.screen.fill((0,0,0))
		pg.draw.rect(self.screen,self.backgroundColor,pg.Rect(np.int(self.leaveEdgeSpace*self.widthLineStepSpace),np.int(self.leaveEdgeSpace*self.heightLineStepSpace),
			np.int(self.gridSize*self.widthLineStepSpace),np.int(self.gridSize*self.heightLineStepSpace)))
		for i in range(self.gridSize+1):
			pg.draw.line(self.screen, self.lineColor, [np.int((i+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int(self.leaveEdgeSpace*self.heightLineStepSpace)],
				[np.int((i+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int((self.gridSize+self.leaveEdgeSpace)*self.heightLineStepSpace)], self.lineWidth)
			pg.draw.line(self.screen, self.lineColor, [np.int(self.leaveEdgeSpace*self.widthLineStepSpace),np.int((i+self.leaveEdgeSpace)*self.heightLineStepSpace)],
				[np.int((self.gridSize+self.leaveEdgeSpace)*self.widthLineStepSpace),np.int((i+self.leaveEdgeSpace)*self.heightLineStepSpace)], self.lineWidth)
		seconds=currentTime/1000
		drawText(self.screen, 'Time: '+str("%4.1f" %seconds)+'s', self.textColorTuple, (self.widthLineStepSpace*2,self.leaveEdgeSpace*10))
		drawText(self.screen, 'Score: '+str(currentScore), self.textColorTuple, (self.widthLineStepSpace*13,self.leaveEdgeSpace*10))
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
	def __call__(self,targetPositionA,targetPositionB,playerPosition,currentTime,currentScore):
		self.drawBackground(currentTime,currentScore)
		pg.draw.circle(self.screen, self.targetColor, [np.int((targetPositionA[0]+self.leaveEdgeSpace+0.5)*self.widthLineStepSpace),
			np.int((targetPositionA[1]+self.leaveEdgeSpace+0.5)*self.heightLineStepSpace)], self.targetRadius)
		pg.draw.circle(self.screen, self.targetColor, [np.int((targetPositionB[0]+self.leaveEdgeSpace+0.5)*self.widthLineStepSpace),
			np.int((targetPositionB[1]+self.leaveEdgeSpace+0.5)*self.heightLineStepSpace)], self.targetRadius)
		pg.draw.circle(self.screen, self.playerColor, [np.int((playerPosition[0]+self.leaveEdgeSpace+0.5)*self.widthLineStepSpace),
			np.int((playerPosition[1]+self.leaveEdgeSpace+0.5)*self.heightLineStepSpace)],self.playerRadius)
		# pg.display.flip()
		return

class DrawImage():
	def __init__(self,screen):
		self.screen=screen
		self.screenCenter=(self.screen.get_width()/2,self.screen.get_height()/2)

	def __call__(self,image):
		imageRect=image.get_rect()
		imageRect.center=self.screenCenter
		pause=True
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP,pg.QUIT])
		self.screen.fill((0, 0, 0))
		self.screen.blit(image, imageRect)
		pg.display.flip()
		while pause:
			pg.time.wait(10)
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
					pause = False
				elif event.type == pg.QUIT:
					pg.quit()
			pg.time.wait(10)
		pg.event.set_blocked([pg.KEYDOWN, pg.KEYUP,pg.QUIT])


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
	currentTime=138456
	currentScore=5
	textColorTuple=(255,50,50)
	drawBackground=DrawBackground(screen, gridSize, leaveEdgeSpace, backgroundColor, lineColor, lineWidth, textColorTuple)
	drawNewState=DrawNewState(screen, drawBackground, targetColor, playerColor, targetRadius, playerRadius)
	drawImage=DrawImage(screen)
	drawBackground(currentTime, currentScore)
	pg.time.wait(5000)
	pg.quit()

>>>>>>> 67e6e0972d5a596e2dd27e6e9dfe81cd4d17d33b
