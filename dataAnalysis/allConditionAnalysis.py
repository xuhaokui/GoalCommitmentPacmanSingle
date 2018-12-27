import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


def listAllCertainFormatOfFile(filePath,fileFormat):
    absolute_filename=[os.path.join(filePath,relative_filename) for relative_filename in os.listdir(filePath)
                       if os.path.isfile(os.path.join(filePath,relative_filename))
                       if os.path.splitext(relative_filename)[1] in fileFormat]
    return absolute_filename


def main():
    resultsPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/Results/'
    fileFormat = [".csv"]
    certainFormatFileName = listAllCertainFormatOfFile(resultsPath, fileFormat)
    allFiles=[pd.DataFrame(pd.read_csv(file)) for file in certainFormatFileName]
    allPersonDataDataFrame=pd.concat(allFiles)
    condition=[-5,-3,-1,0,1,3,5]
    beanEatenFlag=[1,2]
    conditionNumber = [[allPersonDataDataFrame[(allPersonDataDataFrame["condition"] == str(condition[i])) & (allPersonDataDataFrame['beanEaten']==j)].shape[0],condition[i],j] for i in range(len(condition)) for j in beanEatenFlag]
    eatOldGridTrial=[trial[0] for trial in conditionNumber if trial[2]==1]
    eatNewGridTrial=[trial[0] for trial in conditionNumber if trial[2]==2]
    barWidth=0.3
    plt.bar(np.array(condition), eatOldGridTrial, barWidth, color='b',label="oldBean")
    plt.bar(np.array(condition) + barWidth, eatNewGridTrial, barWidth, color='r',label="newBean")
    plt.xlabel('condition')
    plt.xticks(np.array(condition))
    plt.ylabel('trialNumber')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()