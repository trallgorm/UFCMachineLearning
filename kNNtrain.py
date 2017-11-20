import sys
import ScraperDAO
import kNNshared
import random
import math
import itertools
from multiprocessing import Pool
from random import randrange
from datetime import datetime

#Set k to the square root of the amount of samples, a good metric
k = int(math.sqrt(len(ScraperDAO.fighterDifferencesAndResultsList)))
BATCH_SIZE_THRESHOLD = 5



#Fills the training list and the test list with the amount in the training list specified by split percentage
def splitDataset(splitPercentage):
    trainingInstancesList = []
    testInstancesList = []
    data = ScraperDAO.fighterDifferencesAndResultsList
    for i in range(len(data)-1):
        if random.random() < splitPercentage:
            trainingInstancesList.append(data[i])
        else:
            testInstancesList.append(data[i])

    return({"TestList" : testInstancesList, "TrainingList": trainingInstancesList})

#Runs the model and returns its accuracy
def getAccuracyOfModel(statsToJudgeBy):

    datalists = splitDataset(0.66)
    correctGuesses = 0
    for fight in datalists["TestList"]:
        if fight["Result"] == kNNshared.makePrediction(fight, statsToJudgeBy, datalists["TrainingList"], k):
            correctGuesses+=1
    return((correctGuesses/len(datalists["TestList"]))*100)

def readPreviousSession():
    allStats = []
    try:
        with open("top_stats.txt", "r") as topStatsFile:
            for line in topStatsFile:
                if line !='\n' or line!='':
                    lineArray=line.strip().split(',')
                    statArray=lineArray[1:]
                    if '' in statArray:
                        statArray.remove('')
                    accuracy = lineArray[0]
                    allStats.append((statArray,float(accuracy)))
    except FileNotFoundError:
        topStatsFile= open("top_stats.txt", "w+")
    topStatsFile.close()
    return allStats


def writeResultsToFile(statsAndAccuracy):
    file = open('top_stats.txt', 'w+')
    for item in sorted(statsAndAccuracy, key=lambda tup: tup[1], reverse=True):
            file.write(str(item[1]) + "," + str(item[0]).replace("'", "").replace("(", "").replace(")", "").replace(" ", "").replace("[", "").replace("]", "") + '\n')
    file.close()

#Gets the average accuracy of the model
def getAverageAccuracyOfModel(parallelize,statNamesSubset):
        pool = Pool()
        totalaccuracy = 0
        # Runs the model 3 times in parallel to average out the accuracy
        # Parallelized version will speed things up but will require more resources
        # If you want to run it parallelized include -p as a command line argument
        if parallelize:
            result1 = pool.apply_async(getAccuracyOfModel, [statNamesSubset])
            result2 = pool.apply_async(getAccuracyOfModel, [statNamesSubset])
            result3 = pool.apply_async(getAccuracyOfModel, [statNamesSubset])
            totalaccuracy = result1.get() + result2.get() + result3.get()
        # Non parallelized version is slower but requires less resources
        else:
            for i in range(3):
                totalaccuracy += getAccuracyOfModel(statNamesSubset)
        print(str(statNamesSubset) + " : " + str(totalaccuracy / 3))
        return(totalaccuracy / 3)

#Attempts to run the model for a number of stats to see which ones have the most predictive power
#Tries stats names sequentially, starting with the least amount of stats and going to all stats
def trainSequentially(parallelize):
    currentBatchSize = 0
    statsAndAccuracy = readPreviousSession()
    #Runs for a combination of all the stats, will finish in only around 173 trillion years
    for size in range(1, len(ScraperDAO.getNamesOfStats()) + 1):
        for statNamesSubset in itertools.combinations(ScraperDAO.getNamesOfStats(), size):
            currentBatchSize+=1

            statsAndAccuracy.append((statNamesSubset, getAverageAccuracyOfModel(parallelize,statNamesSubset)))
            # Writes the results to a file if the amount of unwritten results has exceeded the threshold
            if (currentBatchSize > BATCH_SIZE_THRESHOLD):
                currentBatchSize = 0
                writeResultsToFile(statsAndAccuracy)

#Attempts to run the model for a number of stats to see which ones have the most predictive power
#Randomly picks stats to check rather than trying them sequentially
def trainRandomly(parallelize):
    statsAndAccuracy =readPreviousSession()
    batchSize = 0

    #Randomly pick a combination of stats and get its accuracy
    while(True):
        statNamesSubset = getRandomCombination(ScraperDAO.getNamesOfStats())
        batchSize+=1
        statsAndAccuracy.append((statNamesSubset,getAverageAccuracyOfModel(parallelize,statNamesSubset)))

        #Writes the results to a file if the amount of unwritten results has exceeded the threshold
        if(batchSize>BATCH_SIZE_THRESHOLD):
            batchSize=0
            writeResultsToFile(statsAndAccuracy)

def trainRandomlyAndSequentially(parallelize):
    statsAndAccuracy =readPreviousSession()
    currentBatchSize = 0

    for size in range(1, len(ScraperDAO.getNamesOfStats()) + 1):
        for statNamesSubset in itertools.combinations(ScraperDAO.getNamesOfStats(), size):
            currentBatchSize += 2

            statsAndAccuracy.append((statNamesSubset, getAverageAccuracyOfModel(parallelize, statNamesSubset)))
            statNamesSubset = getRandomCombination(ScraperDAO.getNamesOfStats())
            statsAndAccuracy.append((statNamesSubset, getAverageAccuracyOfModel(parallelize, statNamesSubset)))
            # Writes the results to a file if the amount of unwritten results has exceeded the threshold
            if (currentBatchSize > BATCH_SIZE_THRESHOLD):
                currentBatchSize = 0
                writeResultsToFile(statsAndAccuracy)


#Test accuracy of using top 100 stats
def testTopStats():
    datalists = splitDataset(0.66)

    correctGuesses = 0
    for fight in datalists["TestList"]:
        win = 0
        loss = 0
        for statArray in kNNshared.readTopStatsFromFile():
            if kNNshared.makePrediction(fight,statArray,ScraperDAO.fighterDifferencesAndResultsList,k)=="Win":
                win+=1
            else:
                loss+=1
        if win>loss:
            predictedFightResult = "Win"
        else:
            predictedFightResult = "Loss"
        if fight["Result"] == predictedFightResult:
            correctGuesses += 1
        print(correctGuesses)

    return ((correctGuesses / len(datalists["TestList"])) * 100)

#Gets a random set of stats given the array of all stats
def getRandomCombination(arrayToPickFrom):
    randomIndex = randrange(1 << len(arrayToPickFrom))
    result = []

    #Each stat has a 50% chance of making it in
    for stat in arrayToPickFrom:
        if randomIndex & 1:
            result.append(stat)
        randomIndex >>= 1
        if randomIndex==0:
            break
    return result

if __name__ ==  '__main__':

    #Use the -p command line option if you want to parallelize the program
    parallelize = False
    if('-p' in sys.argv):
        parallelize = True

    #Use the -s command line optiond if you want to step through the models sequentially rather than randomly
    if('-s' in sys.argv):
        trainSequentially(parallelize)
    else:
        if ('-sr' in sys.argv):
            trainRandomlyAndSequentially(parallelize)
        else:
            trainRandomly(parallelize)












