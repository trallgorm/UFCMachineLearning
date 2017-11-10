import sys
import ScraperDAO
import random
import math
import itertools
from multiprocessing import Pool
from datetime import datetime

#Set k to the square root of the amount of samples, a good metric
k = int(math.sqrt(len(ScraperDAO.fighterDifferencesAndResultsList)))

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

#Gets the euclidean distance between two matches
#Euclidian distance is the root of the sum of the squared differences between the dimensions
def getEuclideanDistance(a, b , stats):
    distance = 0
    for stat in stats:
        if stat!="Result":
            distance += pow((a[stat] - b[stat]), 2)
    return math.sqrt(distance)

#Guesses whether the fighter will win or lose in a fight
#The input is a set of differences between the fighters stats, eg -10 if the opponent is 10 cm taller
def makePrediction(newFight, statsToJudgeBy, trainingInstancesList):


    winDistancesList=[]
    loseDistancesList=[]

    #Gets the distances between all the matches and places them in the win list or the lose list
    for testInstance in trainingInstancesList:
        distance = getEuclideanDistance(testInstance, newFight, statsToJudgeBy)

        #If you ain't first you're last
        if testInstance["Result"]=="Win":
            winDistancesList.append(distance)
        else:
            loseDistancesList.append(distance)

    winDistancesList.sort()
    loseDistancesList.sort()

    winIndex=0
    loseIndex=0

    #Indeces can be thought of as votes. Eg the index for the winlist only moves if the highest current winning distance is lower than the current losing distance
    for x in range(k):
        if winDistancesList[winIndex]<loseDistancesList[loseIndex]:
            winIndex+=1
        else:
            loseIndex+=1


    if(winIndex>loseIndex):
        return("Win")
    else:
        return("Loss")

#Runs the model and returns its accuracy
def getAccuracyOfModel(statsToJudgeBy):

    datalists = splitDataset(0.66)
    correctGuesses = 0
    for fight in datalists["TestList"]:
        if fight["Result"] == makePrediction(fight, statsToJudgeBy, datalists["TrainingList"]):
            correctGuesses+=1
    return((correctGuesses/len(datalists["TestList"]))*100)

def readTopStatsFromFile():
    i=0
    with open("top_stats.txt", "r") as topStatsFile:
        topStats = []
        for line in topStatsFile:
            if i<1000:
                i+=1
                if line !='\n' or line!='':
                    statArray=line.strip().split(',')[1:]
                    if '' in statArray:
                        statArray.remove('')
                    topStats.append(statArray)
            else:
                break
    topStatsFile.close()
    return topStats


def writeResultsToFile(statsAndAccuracy):
    file = open('top_stats.txt', 'w+')
    for item in sorted(statsAndAccuracy, key=lambda tup: tup[1], reverse=True):
            file.write(str(item[1]) + "," + str(item[0]).replace("'", "").replace("(", "").replace(")", "").replace(" ", "") + '\n')
    file.close()

#Attempts to run the model for a number of stats to see which ones have the most predictive power
def testAllStats(parrallelize):
    statsAndAccuracy =[]

    pool = Pool()

    #Runs for a combination of all the stats, will finish in only around 173 trillion years
    for size in range(1, len(ScraperDAO.getNamesOfStats()) + 1):
        batchSize = 0
        for statNamesSubset in itertools.combinations(ScraperDAO.getNamesOfStats(), size):
            batchSize+=1
            totalaccuracy=0

            # Runs the model 3 times in parallel to average out the accuracy
            #Parallelized version will speed things up but will require more resources
            if parrallelize:
                result1 = pool.apply_async(getAccuracyOfModel, [statNamesSubset])
                result2 = pool.apply_async(getAccuracyOfModel, [statNamesSubset])
                result3 = pool.apply_async(getAccuracyOfModel, [statNamesSubset])
                totalaccuracy=result1.get()+result2.get()+result3.get()
            #Non parallelized version is slower but requires less resources
            else:
                for i in range(3):
                    totalaccuracy += getAccuracyOfModel(statNamesSubset)

            statsAndAccuracy.append((statNamesSubset,totalaccuracy/3))
            print(str(statNamesSubset) + " : " + str(totalaccuracy/3))

            #Writes the results to a file if there are over 100 unwritten results just so theres a result to look at if the level doesn't finish
            if(batchSize>100):
                batchSize=0
                writeResultsToFile(statsAndAccuracy)

        print("One level done")
        writeResultsToFile(statsAndAccuracy)

    print("Done")
    return(sorted(statsAndAccuracy, key=lambda tup: tup[1], reverse=True))

#Test accuracy of using top 100 stats
def testTopStats():
    datalists = splitDataset(0.66)

    correctGuesses = 0
    for fight in datalists["TestList"]:
        win = 0
        loss = 0
        for statArray in readTopStatsFromFile():
            if makePrediction(fight,statArray,ScraperDAO.fighterDifferencesAndResultsList)=="Win":
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

#Predicts the outcome of a fight given two fighters
def predictOutcome(fighterNameA,fighterNameB):
    ScraperDAO.getDifferencesBetweenFighters(fighterNameA,fighterNameB)
    win=0
    loss=0
    for statArray in readTopStatsFromFile():
        if makePrediction(ScraperDAO.getDifferencesBetweenFighters(fighterNameA,fighterNameB),statArray,ScraperDAO.fighterDifferencesAndResultsList)=="Win":
            win+=1
        else:
            loss+=1

    if win>loss:
        return (fighterNameA + " wins with " + str(win*100/(win+loss)) + "% accuracy")
    else:
        return (fighterNameB + " wins with " + str(loss*100/(win+loss)) + "% accuracy")

if __name__ ==  '__main__':
    if('-p' in sys.argv):
        print(testAllStats(True))
    else:
        print(testAllStats(False))









