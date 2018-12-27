
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import os 

def createAllCertainFormatFileList(filePath,fileFormat):
	filenameList=[os.path.join(filePath,relativeFilename) for relativeFilename in os.listdir(filePath) 
		if os.path.isfile(os.path.join(filePath,relativeFilename))
		if os.path.splitext(relativeFilename)[1] in fileFormat]
	return filenameList

def cleanDataFrame(rawDataFrame):
	cleanConditionDataFrame=rawDataFrame[rawDataFrame.condition != 'None']
	cleanBeanEatenDataFrame=cleanConditionDataFrame[cleanConditionDataFrame.beanEaten!=0]
	return cleanBeanEatenDataFrame

if __name__=="__main__":
	resultsPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/'
	fileFormat = '.csv'
	resultsFilenameList = createAllCertainFormatFileList(resultsPath, fileFormat)
	resultsDataFrameList = [pd.read_csv(file) for file in resultsFilenameList]
	resultsDataFrame = pd.concat(resultsDataFrameList,sort=False)
	resultsDataFrame=cleanDataFrame(resultsDataFrame)
	participantsTypeList = ['Model' if 'Model' in name else 'Human' for name in resultsDataFrame['name']]
	resultsDataFrame['participantsType']=participantsTypeList
	resultsDataFrame['beanEaten']=resultsDataFrame['beanEaten']-1
	trialNumberEatNewDataFrame = resultsDataFrame.groupby(['name','condition','participantsType']).sum()['beanEaten']
	trialNumberTotalEatDataFrame = resultsDataFrame.groupby(['name','condition','participantsType']).count()['beanEaten']
	mergeConditionDataFrame = pd.DataFrame(trialNumberEatNewDataFrame.values/trialNumberTotalEatDataFrame.values,index=trialNumberTotalEatDataFrame.index,columns=['eatNewPercentage'])
	mergeConditionDataFrame['eatOldPercentage']=1 - mergeConditionDataFrame['eatNewPercentage']
	mergeParticipantsDataFrame = mergeConditionDataFrame.groupby(['condition','participantsType']).mean()
	drawEatOldDataFrame=mergeParticipantsDataFrame['eatOldPercentage'].unstack('participantsType')
	ax=drawEatOldDataFrame.plot.bar(color=['lightsalmon', 'lightseagreen'],ylim=[0.0,1.1])
	ax.set_xlabel('Distance(new - old)',fontweight='bold')
	ax.set_ylabel('Percentage of Eat Old',fontweight='bold')
	plt.show()



