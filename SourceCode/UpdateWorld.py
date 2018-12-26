import numpy as np
from numpy import random
import copy

def indexCertainNumberInList(list, number):
    indexList = [i for i in range(len(list)) if list[i] == number]
    return indexList


def generateRandomGridInSquareArea(squarebBounds):
    grid = [random.randint(squarebBounds[0], squarebBounds[2]),
            random.randint(squarebBounds[1], squarebBounds[3])]
    return grid


def computeAngleBetweenTwoVectors(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    lenthOfVector1 = np.sqrt(vector1.dot(vector1))
    lenthOfVector2 = np.sqrt(vector2.dot(vector2))
    cosAngle = vector1.dot(vector2) / (lenthOfVector1 * lenthOfVector2)
    angle = np.arccos(cosAngle)
    return angle


def generateMeshGridExcludeCertainPoints(squareBounds, excludeGrids):
    [meshGridX, meshGridY] = np.meshgrid(range(squareBounds[0], squareBounds[2]+1, 1),
                                         range(squareBounds[1], squareBounds[3]+1, 1))
    meshGrid = [i for i in zip(meshGridX.flat, meshGridY.flat)]
    validMeshGrid = list(filter(lambda x: x not in excludeGrids, meshGrid))
    valieMeshGridX =np.array([meshGrid[0] for meshGrid in validMeshGrid])
    valieMeshGridY =np.array([meshGrid[1] for meshGrid in validMeshGrid])
    return valieMeshGridX, valieMeshGridY


def generateRandomAreaOutsideAGrid(centerGrid, squareBounds, minDistanceBetweenGrids, excludeGrids=None):
    if excludeGrids is None:
        excludeGrids = []
    meshGridX, meshGridY = generateMeshGridExcludeCertainPoints(squareBounds, excludeGrids)
    distance = abs(meshGridX - centerGrid[0]) + abs(meshGridY - centerGrid[1])
    validGridIndex = np.where(distance >= minDistanceBetweenGrids)
    validGridX = meshGridX[validGridIndex]
    validGridY = meshGridY[validGridIndex]
    return validGridX, validGridY


def sampleAGridFromArea(areaX, areaY):
    randomValidGridIndex = random.choice(range(len(areaX)), 1)
    grid = [areaX[randomValidGridIndex][0], areaY[randomValidGridIndex][0]]
    return grid


def generateRandomGridAtADistanceFromAGrid(centerGrid, squareBounds, radius, excludeGrids=None):
    if excludeGrids is None:
        excludeGrids = []
    meshGridX, meshGridY = generateMeshGridExcludeCertainPoints(squareBounds, excludeGrids)
    distance = abs(meshGridX - centerGrid[0]) + abs(meshGridY - centerGrid[1])
    equalDistanceGridIndex = np.where(distance == radius)
    validGridX = meshGridX[equalDistanceGridIndex]
    validGridY = meshGridY[equalDistanceGridIndex]
    return validGridX, validGridY

class InitialWorld():
    def __init__(self, bounds):
        self.bounds = bounds

    def generateRandomAreaOutsideTwoGrids(self,playerGrid,target1Grid,minDistanceBetweenGrids):
        validTargetGridX1, validTargetGridY1 = generateRandomAreaOutsideAGrid(playerGrid, self.bounds,
                                                                              minDistanceBetweenGrids, [tuple(target1Grid)])
        validTargetGridX2, validTargetGridY2 = generateRandomAreaOutsideAGrid(target1Grid, self.bounds,
                                                                              minDistanceBetweenGrids, [tuple(playerGrid)])
        GridArea1 = list(zip(validTargetGridX1, validTargetGridY1))
        GridArea2 = list(zip(validTargetGridX2, validTargetGridY2))
        intersectionOfGridArea1AndGridArea2 = [str(grid) for grid in GridArea1 if grid in GridArea2]
        target2 = list(eval(np.random.choice(intersectionOfGridArea1AndGridArea2, 1)[0]))
        return target2

    def __call__(self, minDistanceBetweenGrids):
        playerGrid = generateRandomGridInSquareArea(self.bounds)
        validTarget1GridX, validTarget1GridY = generateRandomAreaOutsideAGrid(playerGrid, self.bounds,
                                                                              minDistanceBetweenGrids, [tuple(playerGrid)])
        target1Grid = sampleAGridFromArea(validTarget1GridX, validTarget1GridY)
        target2Grid=self.generateRandomAreaOutsideTwoGrids(playerGrid,target1Grid,minDistanceBetweenGrids)
        return target1Grid, target2Grid, playerGrid


class UpdateWorld():
    def __init__(self, bounds, conditon, counter):
        self.condition = conditon
        self.bounds = bounds
        self.counter = counter
        self.correctionFactors = 0.0001

    def __call__(self, oldTargetGrid, playerGrid):
        counter = copy.deepcopy(self.counter)
        condition = copy.deepcopy(self.condition)
        pause=True
        while pause:
            counterCorrection = [c + self.correctionFactors if c == 0 else c for c in counter]
            sampleProbability = 1 / np.array(counterCorrection)
            normalizeSampleProbability = sampleProbability / np.sum(sampleProbability)
            nextCondition = np.random.choice(condition, 1, p=list(normalizeSampleProbability))[0]
            distance = np.linalg.norm(oldTargetGrid - playerGrid, ord=1) + nextCondition
            validTarget1GridX, validTarget1GridY = generateRandomAreaOutsideAGrid(playerGrid, self.bounds,
                                                                                  distance, [tuple(oldTargetGrid),tuple(playerGrid)])
            if validTarget1GridX.size != 0 and distance!=0 :
                self.counter[condition.index(nextCondition)] = self.counter[condition.index(nextCondition)] + 1
                vectorPlayerGridToValidGrid = list(
                    zip(validTarget1GridX - playerGrid[0], validTarget1GridY - playerGrid[1]))
                vectorPlayerToOldTarget = np.array(oldTargetGrid) - np.array(playerGrid)
                angle = [computeAngleBetweenTwoVectors(vector, vectorPlayerToOldTarget) for vector in
                         vectorPlayerGridToValidGrid]
                maxAngleIndex = indexCertainNumberInList(angle, max(angle))
                gridIndex = np.random.choice(maxAngleIndex, 1)
                newTargetGrid = [validTarget1GridX[gridIndex][0], validTarget1GridY[gridIndex][0]]
                self.counter[condition.index(nextCondition)] = self.counter[condition.index(nextCondition)] + 1
                pause=False
            else:
                invalidConditionIndex = condition.index(nextCondition)
                condition.remove(nextCondition)
                del counter[invalidConditionIndex]
        return newTargetGrid, nextCondition



def main():
    dimension=3
    bounds=[0,0,dimension-1,dimension-1]
    minDistanceBetweenGrids=1
    condition=[-5,-3,-1,0,1,3,5]
    counter=[0]*len(condition)
    action=[0,1]
    initialWorld=InitialWorld(bounds)
    bean1Grid, bean2Grid, humanGrid=initialWorld(minDistanceBetweenGrids)
    updateWorld=UpdateWorld(bounds,condition,counter,minDistanceBetweenGrids)
    nextGrid=updateWorld(bean1Grid,humanGrid,action)

if __name__=="__main__":
    main()
