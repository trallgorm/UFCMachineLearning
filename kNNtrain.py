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
BATCH_SIZE_THRESHOLD = 3

#Runs the model and returns its accuracy
def getAccuracyOfModel(statsToJudgeBy):

    datalists = kNNshared.splitDataset(0.66, ScraperDAO.fighterDifferencesAndResultsList)
    correctGuesses = 0
    for fight in datalists["TestList"]:
        if fight["Result"] == kNNshared.makePrediction(fight, statsToJudgeBy, datalists["TrainingList"], k):
            correctGuesses+=1
    return((correctGuesses/len(datalists["TestList"]))*100)

def writeResultsToFile(statsAndAccuracy):
    file = open('top_stats.txt', 'a+')
    for currentItem in statsAndAccuracy:
            file.write(str(currentItem[1]) + "," + str(currentItem[0]).replace("'", "").replace("(", "").replace(")", "").replace(" ", "").replace("[", "").replace("]", "") + '\n')
    file.close()

#Gets the average accuracy of the model
def getAverageAccuracyOfModel(parallelize,statNamesSubset):
        totalaccuracy = 0
        # Runs the model 3 times in parallel to average out the accuracy
        # Parallelized version will speed things up but will require more resources
        # If you want to run it parallelized include -p as a command line argument
        if parallelize:
            pool = Pool()
            result1 = pool.apply_async(getAccuracyOfModel, [statNamesSubset])
            result2 = pool.apply_async(getAccuracyOfModel, [statNamesSubset])
            result3 = pool.apply_async(getAccuracyOfModel, [statNamesSubset])
            totalaccuracy = result1.get() + result2.get() + result3.get()
            pool.close()
        # Non parallelized version is slower but requires less resources
        else:
            for i in range(3):
                totalaccuracy += getAccuracyOfModel(statNamesSubset)
        print(str(totalaccuracy / 3) + " : " + str(statNamesSubset))
        return(totalaccuracy / 3)

#Attempts to run the model for a number of stats to see which ones have the most predictive power
#Tries stats names sequentially, starting with the least amount of stats and going to all stats
def trainSequentially(parallelize):
    currentBatchSize = 0
    statsAndAccuracy = []
    #Runs for a combination of all the stats, will finish in only around 173 trillion years
    for size in range(1, len(ScraperDAO.getNamesOfStats()) + 1):
        for statNamesSubset in itertools.combinations(ScraperDAO.getNamesOfStats(), size):
            currentBatchSize+=1

            statsAndAccuracy.append((statNamesSubset, getAverageAccuracyOfModel(parallelize,statNamesSubset)))
            # Writes the results to a file if the amount of unwritten results has exceeded the threshold
            if (currentBatchSize > BATCH_SIZE_THRESHOLD):
                currentBatchSize = 0
                writeResultsToFile(statsAndAccuracy)
                statsAndAccuracy = []

#Attempts to run the model for a number of stats to see which ones have the most predictive power
#Randomly picks stats to check rather than trying them sequentially
def trainRandomly(parallelize):
    statsAndAccuracy =[]
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
            statsAndAccuracy = []

#Attempts to run the model for a number of stats to see which ones have the most predictive power
#Goes through the stats sequentially but also picks one stat at random for every sequential one
def trainRandomlyAndSequentially(parallelize):
    statsAndAccuracy = []
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
                statsAndAccuracy = []

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












