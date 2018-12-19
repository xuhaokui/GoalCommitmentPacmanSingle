import numpy as np
from numpy import random

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
    angle = np.arccos(cosAngle) / 2 / pi * 360
    return angle


def generateMeshGridExcludeCertainPoints(squareBounds, *excludeGrids):
    [meshGridX, meshGridY] = np.meshgrid(range(squareBounds[0], squareBounds[2], 1),
                                         range(squareBounds[1], squareBounds[3], 1))
    meshGrid = [i for i in zip(meshGridX.flat, meshGridY.flat)]
    validMeshGrid = list(filter(lambda x: x not in excludeGrids, meshGrid))
    valieMeshGridX = np.array([meshGrid[0] for meshGrid in validMeshGrid])
    valieMeshGridY = np.array([meshGrid[1] for meshGrid in validMeshGrid])
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

    def __call__(self, minDistanceBetweenGrids):
        playerGrid = generateRandomGridInSquareArea(self.bounds)
        validTarget1GridX, validTarget1GridY = generateRandomAreaOutsideAGrid(playerGrid, self.bounds,
                                                                              minDistanceBetweenGrids, [playerGrid])
        target1Grid = sampleAGridFromArea(validTarget1GridX, validTarget1GridY)
        validTarget2GridX, validTarget2GridY = generateRandomAreaOutsideAGrid(playerGrid, self.bounds,
                                                                              minDistanceBetweenGrids, [target1Grid])
        target2Grid = sampleAGridFromArea(validTarget2GridX, validTarget2GridY)
        return target1Grid, target2Grid, playerGrid


class UpdateWorld():
    def __init__(self, bounds, conditon, counter, minDistanceBetweenGrids):
        self.condition = conditon
        self.index=0
        self.bounds = bounds
        self.counter = counter
        self.minDistanceBetweenGrids = minDistanceBetweenGrids
        self.errorIndex=[]
        self.correctionFactors = 0.0001

    def calculateSampleConditionProbability(self, condition, counter):
        try:
            counterCorrection = [c + self.correctionFactors for c in counter if c == 0]
            sampleProbability = 1 / np.array(counterCorrection)
            normalizeSampleProbability = sampleProbability / np.sum(sampleProbability)
            sampledCondition = np.random.choice(condition, 1, p=list(normalizeSampleProbability))[0]
            return sampledCondition
        except ValueError as e:
            return None

    def generateValidNewGrid(self, playerGrid, oldTargetGrid, radius):
        randomGridX, randomGridY = generateRandomGridAtADistanceFromAGrid(playerGrid, self.bounds, radius,
                                                                          excludeGrids=[oldTargetGrid, playerGrid])
        correctedPlayerGrid = [coordinate + self.correctionFactors for coordinate in playerGrid]
        meshGridDirection = (randomGridY - correctedPlayerGrid[1]) / (randomGridX - correctedPlayerGrid[0])
        TargetDirection = (oldTargetGrid[1] - correctedPlayerGrid[1]) / (oldTargetGrid[0] - correctedPlayerGrid[0])
        relativeDirectionBetweenTargetAndmeshGrid = meshGridDirection * TargetDirection
        validGridIndex = np.where(relativeDirectionBetweenTargetAndmeshGrid < 0)
        validGridX = randomGridX[validGridIndex]
        validGridY = randomGridY[validGridIndex]
        return validGridX, validGridY

    def calculateNextCondition(self, playerGrid, oldTargetGrid, condition, counter):
        try:
            nextCondition = self.calculateSampleConditionProbability(condition, counter)
            distance = np.linalg.norm(oldTargetGrid - playerGrid, ord=1) + nextCondition
            validGridX, validGridY = self.generateValidNewGrid(playerGrid, oldTargetGrid, distance)
            if validGridX.size == 0:
                invalidConditionIndex = condition.index(nextCondition)
                condition.remove(nextCondition)
                del counter[invalidConditionIndex]
                return self.calculateNextCondition(playerGrid, oldTargetGrid, condition, counter)
            else:
                return nextCondition
        except IndexError :
            return None
        except TypeError :
            return None

    def generateNextGrid(self, playerGrid, oldTargetGrid, condition, playerAction, angleBetweenActionAndOldTarget):
        distanceBetweenOldTargetToHuman = np.linalg.norm(oldTargetGrid - playerGrid, ord=1)
        nextDistance = distanceBetweenOldTargetToHuman + condition
        validGridX, validGridY = self.generateValidNewGrid(playerGrid, oldTargetGrid, nextDistance)
        vectorBetweenPlayerGridToValidGrid = list(zip(validGridX - playerGrid[0], validGridY - playerGrid[1]))
        angle = [abs(computeAngleBetweenTwoVectors(vector, playerAction) - angleBetweenActionAndOldTarget)
                 for vector in vectorBetweenPlayerGridToValidGrid]
        minAngleIndex = indexCertainNumberInList(angle, min(angle))
        gridIndex = np.random.choice(minAngleIndex, 1)
        grid = [validGridX[gridIndex][0], validGridY[gridIndex][0]]
        return grid

    def __call__(self, oldTargetGrid, playerGrid, playerAction):
        counter = self.counter
        condition = self.condition
        self.index=self.index+1
        oldTargetGrid = np.array(oldTargetGrid)
        playerGrid = np.array(playerGrid)
        vectorPlayerToOldTarget = oldTargetGrid - playerGrid
        angleBetweenActionAndOldTarget = computeAngleBetweenTwoVectors(playerAction, vectorPlayerToOldTarget)
        nextCondition = self.calculateNextCondition(playerGrid, oldTargetGrid, condition, counter)
        if nextCondition is not None:
            self.counter[condition.index(nextCondition)] = self.counter[condition.index(nextCondition)] + 1
            newTargetGrid = self.generateNextGrid(playerGrid, oldTargetGrid, nextCondition, playerAction,
                                                  angleBetweenActionAndOldTarget)
        else:
            validTargetGridX, validTargetGridY = generateRandomAreaOutsideAGrid(playerGrid, self.bounds,
                                                                                self.minDistanceBetweenGrids,
                                                                                [playerGrid,oldTargetGrid])
            newTargetGrid = sampleAGridFromArea(validTargetGridX, validTargetGridY)
            self.errorIndex.append(self.index)
        return newTargetGrid
