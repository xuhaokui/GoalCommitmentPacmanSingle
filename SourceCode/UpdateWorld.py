import random
import numpy as np
import copy

def computeAngleBetweenTwoVectors(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    lenthOfVector1 = np.sqrt(vector1.dot(vector1))
    lenthOfVector2 = np.sqrt(vector2.dot(vector2))
    cosAngle = vector1.dot(vector2) / (lenthOfVector1 * lenthOfVector2)
    angle = np.arccos(cosAngle)
    return angle

def indexCertainNumberInList(list, number):
    indexList = [i for i in range(len(list)) if list[i] == number]
    return indexList

class InitialWorld():
    def __init__(self, bounds):
        self.bounds = bounds

    def __call__(self,minDistanceBetweenGrids):
        playerGrid = [random.randint(self.bounds[0], self.bounds[2]),
                random.randint(self.bounds[1], self.bounds[3])]
        [meshGridX, meshGridY] = np.meshgrid(range(self.bounds[0], self.bounds[2] + 1, 1),
                                             range(self.bounds[1], self.bounds[3] + 1, 1))
        distanceOfPlayerGrid=abs(meshGridX-playerGrid[0])+abs(meshGridY-playerGrid[1])
        target1GridArea=np.where(distanceOfPlayerGrid>minDistanceBetweenGrids)
        target1GridIndex=random.randint(0,len(target1GridArea[0])-1)
        target1Grid=[meshGridX[target1GridArea[0][target1GridIndex]][target1GridArea[1][target1GridIndex]],
                               meshGridY[target1GridArea[0][target1GridIndex]][target1GridArea[1][target1GridIndex]]]
        distanceOfTarget1Grid=abs(meshGridX-target1Grid[0])+abs(meshGridY-target1Grid[1])
        target2GridArea = np.where((distanceOfPlayerGrid > minDistanceBetweenGrids) * (distanceOfTarget1Grid  > minDistanceBetweenGrids)==True)
        target2GridIndex=random.randint(0,len(target2GridArea[0])-1)
        target2Grid=[meshGridX[target2GridArea[0][target2GridIndex]][target2GridArea[1][target2GridIndex]],
                               meshGridY[target2GridArea[0][target2GridIndex]][target2GridArea[1][target2GridIndex]]]
        return target1Grid,target2Grid,playerGrid

class UpdateWorld():
    def __init__(self, bounds, conditon, counter):
        self.condition = conditon
        self.bounds = bounds
        self.counter = counter
        self.correctionFactors = 0.0001

    def __call__(self, oldTargetGrid, playerGrid):
        counter = copy.deepcopy(self.counter)
        condition = copy.deepcopy(self.condition)
        pause = True
        while pause:
            counterCorrection = [c + self.correctionFactors if c == 0 else c for c in counter]
            sampleProbability = 1 / np.array(counterCorrection)
            normalizeSampleProbability = sampleProbability / np.sum(sampleProbability)
            nextCondition = np.random.choice(condition, 1, p=list(normalizeSampleProbability))[0]
            distance = np.linalg.norm(np.array(oldTargetGrid) - np.array(playerGrid), ord=1) + nextCondition
            [meshGridX, meshGridY] = np.meshgrid(range(self.bounds[0], self.bounds[2] + 1, 1),
                                                 range(self.bounds[1], self.bounds[3] + 1, 1))
            distanceOfPlayerGrid = abs(meshGridX - playerGrid[0]) + abs(meshGridY - playerGrid[1])
            distanceOfOldTargetGrid = abs(meshGridX - oldTargetGrid[0]) + abs(meshGridY - oldTargetGrid[1])
            newTargetGridArea = np.where((distanceOfPlayerGrid == distance) * (
                    distanceOfOldTargetGrid > 1) == True)
            if len(newTargetGridArea[0])!= 0 and distance != 0:
                newTargetGridArea = [[meshGridX[newTargetGridArea[0][index]][newTargetGridArea[1][index]],
                               meshGridY[newTargetGridArea[0][index]][newTargetGridArea[1][index]]] for index in range(len(newTargetGridArea[0]))]
                vectorBetweenNewTargetAndPlayer=[np.array(target)-np.array(playerGrid) for target in newTargetGridArea]
                vectorBetweenOldTargetAndPlayer=np.array(oldTargetGrid)-np.array(playerGrid)
                angle = [computeAngleBetweenTwoVectors(vector, vectorBetweenOldTargetAndPlayer) for vector in
                         vectorBetweenNewTargetAndPlayer]
                maxAngleIndex = indexCertainNumberInList(angle, max(angle))
                gridIndex = np.random.choice(maxAngleIndex, 1)
                newTargetGrid = newTargetGridArea[gridIndex[0]]
                self.counter[condition.index(nextCondition)] = self.counter[condition.index(nextCondition)] + 1
                pause=False
            else:
                invalidConditionIndex = condition.index(nextCondition)
                condition.remove(nextCondition)
                del counter[invalidConditionIndex]

        return newTargetGrid,nextCondition



def main():
    dimension = 15
    bounds = [0, 0, dimension - 1, dimension - 1]
    condition = [-5, -3, -1, 0, 1, 3, 5]
    counter = [0] * len(condition)
    minDistanceBetweenGrids=1
    initialWorld=InitialWorld(bounds)
    target1Grid, target2Grid, playerGrid=initialWorld(minDistanceBetweenGrids)
    updateWorld=UpdateWorld(bounds,condition,counter)
    target2Grid,nextCondition=updateWorld(target1Grid,playerGrid)
    print(playerGrid,target2Grid,nextCondition)

if __name__=="__main__":
    main()
