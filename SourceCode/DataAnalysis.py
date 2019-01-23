import pandas as pd
import matplotlib.pyplot as plt
import os
import pylab as pl
import numpy as np
from scipy import stats,optimize
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.optimize import curve_fit
from scipy import log


def createAllCertainFormatFileList(filePath,fileFormat):
	filenameList=[os.path.join(filePath,relativeFilename) for relativeFilename in os.listdir(filePath)
		if os.path.isfile(os.path.join(filePath,relativeFilename))
		if os.path.splitext(relativeFilename)[1] in fileFormat]
	return filenameList

def cleanDataFrame(rawDataFrame):
	cleanConditionDataFrame=rawDataFrame[rawDataFrame.condition != 'None']
	cleanBeanEatenDataFrame=cleanConditionDataFrame[cleanConditionDataFrame.beanEaten!=0]
	return cleanBeanEatenDataFrame


def weibullFunction( x,k, c):
    return k * log(x) + c

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
    mergeParticipantsDataFrameMean = mergeConditionDataFrame.groupby(['condition','participantsType']).mean()
    mergeParticipantsDataFrameStandardError = mergeConditionDataFrame.groupby(['condition', 'participantsType']).std()
    mergeConditionDataFrame.groupby(['condition', 'participantsType'])
    drawEatOldDataFrameMean=mergeParticipantsDataFrameMean['eatOldPercentage'].unstack('participantsType')
    orderedCondition=['-5','-3','-1','0','1','3','5']
    condition=np.array([eval(c) for c in orderedCondition])
    drawEatOldDataFrameMean['orderedCondition']=drawEatOldDataFrameMean.index
    drawEatOldDataFrameMean['orderedCondition']=drawEatOldDataFrameMean['orderedCondition'].astype('category')
    drawEatOldDataFrameMean['orderedCondition'].cat.reorder_categories(orderedCondition,inplace=True)
    drawEatOldDataFrameMean.sort_values('orderedCondition',inplace=True)
    drawEatOldDataFrameError=mergeParticipantsDataFrameStandardError['eatOldPercentage'].unstack('participantsType')
    drawEatOldDataFrameMean.index=condition
    # ax=drawEatOldDataFrameMean.plot.scatter(y='Human',x= drawEatOldDataFrameMean.index)
    # plt.show()
    modelResult=list(drawEatOldDataFrameMean["Model"])
    humanResult=list(drawEatOldDataFrameMean["Human"])
    print(humanResult)
    # plt.plot(humanResult,condition)
    fitKModel, fitCModel = optimize.curve_fit(weibullFunction, np.array(modelResult)*100, np.array(condition))[0]
    fitKHuman, fitCHuman = optimize.curve_fit(weibullFunction, np.array(humanResult)*100, np.array(condition))[0]
    print(fitKHuman,fitCHuman)
    modelCurveFit=fitKModel*log(condition)+fitCModel
    humanCurveFit=fitKHuman*log(condition)+fitCHuman
    # plt.plot(condition, modelCurveFit, "purple")
    # plt.xlim((-7, 7))
    # plt.ylim((-30, 30))
    plt.plot(condition, modelCurveFit, "black")
    plt.show()

    # ax=drawEatOldDataFrameMean.plot.scatter(yerr=drawEatOldDataFrameError,color=['lightsalmon', 'lightseagreen'],ylim=[0.0,1.1],width=0.8)
    # pl.xticks(rotation=0)
    # plt.yticks(np.arange(0, 1.1, 0.1))
    # ax.set_xlabel('Distance(new - old)',fontweight='bold')
    # ax.set_ylabel('Percentage of Eat Old',fontweight='bold')
    # plt.show()
    # mergeConditionDataFrame["level"].describe().reset_index()
    # mergeConditionDataFrame = mergeConditionDataFrame.reset_index(level=["name", 'condition', 'participantsType'])
    # mergeConditionDataFrame['eatOldPercentage'] = 1 - mergeConditionDataFrame['eatNewPercentage']
    # cw_lm = ols('eatOldPercentage ~ participantsType + condition+participantsType:condition',
    #             data=mergeConditionDataFrame).fit()
    # print(type(sm.stats.anova_lm(cw_lm, typ=2)))
    # print(pairwise_tukeyhsd(mergeConditionDataFrame['eatOldPercentage'],mergeConditionDataFrame['condition']))

