import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import os
import pylab as pl

def createAllCertainFormatFileList(filePath,fileFormat):
	filenameList=[os.path.join(filePath,relativeFilename) for relativeFilename in os.listdir(filePath)
		if os.path.isfile(os.path.join(filePath,relativeFilename))
		if os.path.splitext(relativeFilename)[1] in fileFormat]
	return filenameList

def cleanDataFrame(rawDataFrame):
	cleanConditionDataFrame=rawDataFrame[rawDataFrame.condition != 'None']
	cleanBeanEatenDataFrame=cleanConditionDataFrame[cleanConditionDataFrame.beanEaten!=0]
	cleanbRealConditionDataFrame=cleanBeanEatenDataFrame.loc[cleanBeanEatenDataFrame['realCondition'].isin(range(-5,6))]
	return cleanbRealConditionDataFrame

def calculateRealCondition(rawDataFrame):
	rawDataFrame['realCondition']=(np.abs(rawDataFrame['bean2GridX'] - rawDataFrame['playerGridX'])+np.abs(rawDataFrame['bean2GridY'] - rawDataFrame['playerGridY']))-(np.abs(rawDataFrame['bean1GridX'] - rawDataFrame['playerGridX'])+np.abs(rawDataFrame['bean1GridY'] - rawDataFrame['playerGridY']))
	newDataFrameWithRealCondition=rawDataFrame.copy()
	return newDataFrameWithRealCondition

if __name__=="__main__":
	resultsPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/'
	fileFormat = '.csv'
	resultsFilenameList = createAllCertainFormatFileList(resultsPath, fileFormat)
	resultsDataFrameList = [pd.read_csv(file) for file in resultsFilenameList]
	resultsDataFrame = pd.concat(resultsDataFrameList,sort=False)
	resultsDataFrame=calculateRealCondition(resultsDataFrame)
	resultsDataFrame=cleanDataFrame(resultsDataFrame)
	participantsTypeList = ['Model' if 'Model' in name else 'Human' for name in resultsDataFrame['name']]
	resultsDataFrame['participantsType']=participantsTypeList
	resultsDataFrame['beanEaten']=resultsDataFrame['beanEaten']-1
	trialNumberEatNewDataFrame = resultsDataFrame.groupby(['name','realCondition','participantsType']).sum()['beanEaten']
	trialNumberTotalEatDataFrame = resultsDataFrame.groupby(['name','realCondition','participantsType']).count()['beanEaten']
	mergeConditionDataFrame = pd.DataFrame(trialNumberEatNewDataFrame.values/trialNumberTotalEatDataFrame.values,index=trialNumberTotalEatDataFrame.index,columns=['eatNewPercentage'])
	mergeConditionDataFrame['eatOldPercentage']=1 - mergeConditionDataFrame['eatNewPercentage']
	mergeParticipantsDataFrame = mergeConditionDataFrame.groupby(['realCondition','participantsType']).mean()
	drawEatOldDataFrame=mergeParticipantsDataFrame['eatOldPercentage'].unstack('participantsType')
	ax=drawEatOldDataFrame.plot.bar(color=['lightsalmon', 'lightseagreen'],ylim=[0.0,1.1],width=0.8)
	pl.xticks(rotation=0)
	ax.set_xlabel('Distance(new - old)',fontweight='bold')
	ax.set_ylabel('Percentage of Eat Old',fontweight='bold')
	plt.show()